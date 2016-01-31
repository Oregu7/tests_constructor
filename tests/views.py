from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from django.forms.models import model_to_dict
from testsConstructor.helpers import check_sign_in, models_to_dict, str_to_bool
from constructor.models import Test, Query, Answer
from tests.models import Probationer
import json
import random
# Create your views here.

def tests(request):
	login = check_sign_in(request)
	tests = Test.objects.filter(public_access=True)[:15]
	data = [tests[:5], tests[5:10], tests[10:15]]
	return render_to_response('tests.html', {'data': data, 'login': login})

@csrf_exempt	
def set_name(request):
	if request.is_ajax() and 'test' in request.session:
		request.session.modified = True
		request.session['test']['user'] = request.POST['user']
		return JsonResponse({'success': True})
	else:
		raise Http404('Такая страница не существует')

@csrf_exempt
def search(request):
	login = check_sign_in(request)
	tests = Test.objects.filter(title__icontains=request.GET['search_text'])[:15]
	data = models_to_dict(tests)
	return HttpResponse(json.dumps(data))

@csrf_exempt
def test(request, id):
	login = check_sign_in(request)
	test = get_object_or_404(Test, id=id, public_access=True)
	if request.is_ajax():
		#Если не существует сессии с данным тестом , мы ее создаем
		if 'test' not in request.session or request.session['test']['id'] != test.id:
			questions = models_to_dict(Query.objects.filter(test=test).order_by('?')[:5])
			random.shuffle(questions)

			request.session['test'] = {
				'id': test.id,
				'questions' : list(map(lambda quest: quest['id'], questions)),
				'answers' : [],
				'current_quset': 0,
				'user': 'Гость'
			}

		quest = Query.objects.get(id=request.session['test']['questions'][request.session['test']['current_quset']])
		answers = models_to_dict(Answer.objects.filter(query=quest))
		random.shuffle(answers)
		#проверяем включены ли подсказки и время сдачи
		test = model_to_dict(test)
		quest = model_to_dict(quest)
		if not test['time_completion']:
			quest['time'] = False
		if not test['helps']:
			quest['help'] = False

		return HttpResponse(json.dumps({'quest': quest, 'answers': answers}))
	else:
		return render_to_response('test.html', {'login': login, 'test': test})

@csrf_exempt
def test_next_quest(request):
	if request.is_ajax():
		if 'test' in request.session:
			#Включаем возможность модификации сесии
			request.session.modified = True
			#сохраняем ответы
			answers = list(map(lambda answer: {'id': answer['id'], 'selection': answer['selection']},json.loads(request.POST['answers'])))
			request.session['test']['answers'].append(answers)
			#отдаем следующий вопрос или завершаем тест
			next_question = request.session['test']['current_quset'] + 1
			if next_question <= len(request.session['test']['questions']) - 1:
				#увеличиваем индекс текущего вопроса
				request.session['test']['current_quset'] = next_question
				#находим данные
				test = Test.objects.get(id=request.session['test']['id'])
				quest = Query.objects.get(id=request.session['test']['questions'][next_question], test=test)
				answers = models_to_dict(Answer.objects.filter(query=quest))
				random.shuffle(answers)
				#проверяем включены ли подсказки и время сдачи
				test = model_to_dict(test)
				quest = model_to_dict(quest)
				if not test['time_completion']:
					quest['time'] = False
				if not test['helps']:
					quest['help'] = False

				return HttpResponse(json.dumps({'quest': quest, 'answers': answers}))
			else:
				#расчитываем результаты
				test_data = request.session['test']
				test = Test.objects.get(id=test_data['id'])
				max_points = 0
				user_points = 0
				#начинаем обработку вопросов и ответов
				for num in range(len(request.session['test']['questions'])):
					question = Query.objects.get(id=test_data['questions'][num])
					point = model_to_dict(question)['point']
					max_points += point
					#перебираем ответы
					for answer in test_data['answers'][num]:
						answer_data = model_to_dict(Answer.objects.get(id=answer['id'],query=question))
						if answer_data['correct'] != answer['selection']:
							break
					else:
						user_points += point

				#получаем процент
				user_percent = user_points * 100 / max_points
				test = model_to_dict(test)

				if user_percent >= 0 and user_percent < test['two_mark']:
					color = 'red'
					result = 2
				elif user_percent >= test['two_mark'] and user_percent < test['three_mark']:
					color = 'yellow'
					result = 3
				elif user_percent >= test['three_mark'] and user_percent < test['four_mark']:
					color = 'blue'
					result = 4
				else:
					color = 'green'
					result = 5

				#создаем объект тестируемого
				probationer = Probationer(
					test = Test.objects.get(id=test['id']),
					name = test_data['user'],
					precent = user_percent,
					mark = result
				)
				probationer.save()
				#удаляем сессию
				del request.session['test']

				return HttpResponse(json.dumps({'test_result': result, 'color': color}))
		else:
			raise Http404('Отсутствует сессия')
	else:
		raise Http404('Такая страница не существует!')