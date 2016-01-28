from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from django.forms.models import model_to_dict
from testsConstructor.helpers import check_sign_in, models_to_dict
from constructor.models import Test, Query, Answer
import json
import random
# Create your views here.
def tests(request):
	login = check_sign_in(request)
	tests = Test.objects.all()[:15]
	data = [tests[:5], tests[5:10], tests[10:15]]
	return render_to_response('tests.html', {'data': data, 'login': login})

def search(request):
	#login = check_sign_in(request)
	#tests = Test.objects.filter(title__icontains=request.GET['search_text'])[:15]
	#data = models_to_dict(tests)
	return JsonResponse(request.session['test'])
	#return HttpResponse(json.dumps(data))

def test(request, id):
	login = check_sign_in(request)
	test = get_object_or_404(Test, id=id)
	if request.is_ajax():
		#Если не существует сессии с данным тестом , мы ее создаем
		if 'test' not in request.session or request.session['test']['id'] != test.id:
			questions = models_to_dict(Query.objects.filter(test=test).order_by('?')[:5])
			random.shuffle(questions)

			request.session['test'] = {
				'id': test.id,
				'questions' : list(map(lambda quest: quest['id'], questions)),
				'answers' : [],
				'current_quset': 0
			}

		quest = Query.objects.get(id=request.session['test']['questions'][request.session['test']['current_quset']])
		answers = models_to_dict(Answer.objects.filter(query=quest))
		return HttpResponse(json.dumps({'quest': model_to_dict(quest), 'answers': answers}))
	else:
		return render_to_response('test.html', {'login': login, 'test': test})

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
				request.session['test']['current_quset'] = next_question
				quest = Query.objects.get(id=request.session['test']['questions'][next_question])
				answers = models_to_dict(Answer.objects.filter(query=quest))

				return HttpResponse(json.dumps({'quest': model_to_dict(quest), 'answers': answers}))
			else:
				#расчитываем результаты
				return JsonResponse({'msg': 'test is complite'})
		else:
			raise Http404('Отсутствует сессия')
	else:
		raise Http404('Такая страница не существует!')