from django.shortcuts import render_to_response, redirect, get_object_or_404
from testsConstructor.helpers import check_sign_in, str_to_bool
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from constructor.models import Test, Query, Answer
from users.models import Users
import json

def get_answers(query):
	answers = Answer.objects.filter(query=query)

	result = {
		'query': query,
		'answers': {
			'all': len(answers),
			'correct': len(list(filter(lambda answer: answer.correct, answers)))
		}
	}

	return result

def create_test(request):
	if request.is_ajax():
		try:
			user = Users.objects.get(login=request.session.get('user'))
			test = Test(
				title = request.POST['title'],
				description = request.POST['description'],
				helps = str_to_bool(request.POST['helps']),
				time_completion = str_to_bool(request.POST['timeCompl']),
				creator = user,
				two_mark = request.POST['two_mark'],
				three_mark = request.POST['three_mark'],
				four_mark = request.POST['four_mark']
			)
			test.save()

			return JsonResponse({'testID': test.id, 'error': False})
		except ObjectDoesNotExist:
			return JsonResponse({'error': True})
	elif 'user' in request.session:
		sign_in = check_sign_in(request)
		return render_to_response('create_test.html', {'login': sign_in})
	else:
		return redirect('/')

def settings_test(request, id):
	test = get_object_or_404(Test, id=id)
	login = check_sign_in(request)
	if test.creator == get_object_or_404(Users, login=login):
		if request.is_ajax():

			test.title = request.POST['title']
			test.description = request.POST['description']
			test.helps = str_to_bool(request.POST['helps'])
			test.time_completion = str_to_bool(request.POST['timeCompl'])
			test.two_mark = request.POST['two_mark']
			test.three_mark = request.POST['three_mark']
			test.four_mark = request.POST['four_mark']

			test.save()

			return JsonResponse({'success': 'Данные сохранены!'})
		else:
			return render_to_response('create_test.html', {'login': login, 'test': test})
	else:
		return redirect('/')

def queries_test(request, id):
	sign_in = check_sign_in(request)
	test = Test.objects.get(id=id)
	queries = map(get_answers, Query.objects.filter(test = test))

	return render_to_response('test/queries.html', {'login': sign_in, 'test': test, 'queries': queries})

def add_query(request, id):
	login = check_sign_in(request)
	if login:
		try:
			test = Test.objects.get(id=int(id))
			if test.creator.login == login:
				#кодим тут (когда все True)
				if request.is_ajax():
					query = Query(
						test = test,
						text = request.POST['text'],
						point = request.POST['point'],
						helps = request.POST['help'],
						time = request.POST['time']
					)

					query.save()
					for data_answer in json.loads(request.POST['answers']):
						answer = Answer(
							query = query,
							text = data_answer['text'],
							correct = data_answer['correct']
						)

						answer.save()

					return JsonResponse({'complite': True})
				else:	
					return render_to_response('add_query.html', {'login': login, 'test': test})
			else:
				raise Http404('Вы не являетесь создателем данного теста!')
		except:
			raise Http404('Теста с таким id не существует!')
	else:
		return redirect('/')

def delete_query(request, t_id, q_id):
	Query.objects.get(test=t_id, id=q_id).delete()
	return redirect('/constructor/test/' + t_id + '/questions/')

def edit_question(request, t_id, q_id):
	test = get_object_or_404(Test, id=t_id)
	question = get_object_or_404(Query, id=q_id)
	answers = Answer.objects.filter(query=question)
	login = check_sign_in(request)

	if test.creator.login == login:
		if request.is_ajax():
			response = []
			#получаем поля модели в json формате и сразу парсим
			answers = json.loads(serializers.serialize('json', answers))
			#формируем модели
			for answer in answers:
				data = answer.get('fields')
				data['id'] = answer.get('pk')
				response.append(data)
			#возвращаем модели в JSON формате
			return HttpResponse(json.dumps(response))
		else:
			return render_to_response('add_query.html', 
				{
					'login': login, 
					'test': test, 
					'question': question,
					'answers': answers
				}
			)
	else:
		return Http404('Вы не являетесь создателем данного теста!')

def question_actions(request, qid, aid):
	if request.method == 'DELETE':
		answer = get_object_or_404(Answer, query=qid, id=aid)
		answer.delete()
		return JsonResponse({'msg':'delete'})
	elif request.method == 'PUT':
		answer = get_object_or_404(Answer, query=qid, id=aid)
		#парсим put запрос
		put = json.loads(list(QueryDict(request.body).dict().keys())[0])
		#обновляем данные
		answer.text = put.get('text')
		answer.correct = put.get('correct')
		answer.save()

		return JsonResponse({'msg':'success'})
	elif request.method == 'POST':
		question = get_object_or_404(Query, id=qid)
		answer = Answer(query=question)

		answer.save()
		return JsonResponse({'id': answer.id})