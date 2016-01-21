from django.shortcuts import render_to_response, redirect
from testsConstructor.helpers import check_sign_in
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
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
				helps = request.POST['helps'],
				time_completion = request.POST['timeCompl'],
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
	sign_in = check_sign_in(request)
	test = Test.objects.get(id=id)
	queries = map(get_answers, Query.objects.filter(test = test))

	return render_to_response('test/queries.html', {'login': sign_in, 'test': test, 'queries': queries})

def add_query(request, id):
	login = check_sign_in(request)
	if login:
		try:
			test = Test.objects.get(id=id)
			if test.creator.login == login:
				#кодим тут (когда все True)
				if request.is_ajax():
					query = Query(
						test = test,
						text = request.POST['text'],
						point = request.POST['point']
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