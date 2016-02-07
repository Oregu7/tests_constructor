from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from django.forms.models import model_to_dict
from testsConstructor.helpers import check_sign_in, models_to_dict, str_to_bool, get_number_name
from constructor.models import Test, Query, Answer, Category
from django.core.paginator import Paginator
from tests.models import Probationer
import json
import random
import datetime
# Create your views here.

def tests(request, category = 'all', page_number = 1):
	login = check_sign_in(request)
	categories = Category.objects.all()
	args = {'login': login, 'categories': categories, 'tests_category': category}
	args.update(csrf(request))

	#удаляем сессию поиска, если присутствует
	if 'search' in request.session:
		del request.session['search']

	if request.method == 'GET':
		#Проверка категории
		if category == 'all':
			tests = Test.objects.filter(public_access=True)
			args['url'] = '/tests/page/'
		else:
			tests = Test.objects.filter(public_access=True, category__url=category)
			args['url'] = '/tests/category/%s/page/' % category
	elif request.method == 'POST':
		title = request.POST.get('search', '')
		request.session['search'] = {'text': title, 'category': category}
		return redirect('/tests/search/')
	#Пагинация
	current_page = Paginator(tests, 15)
	if int(page_number) > current_page.num_pages or int(page_number) < 1:
		raise Http404('Такой страницы нет')

	args['tests'] = current_page.page(page_number)
	args['pages_count'] = get_number_name(current_page.num_pages + 2)
	return render_to_response('tests.html', args)

@csrf_exempt	
def set_name(request):
	if request.is_ajax() and 'test' in request.session:
		request.session.modified = True
		request.session['test']['user'] = request.POST['user']

		#если пользователь зареган, то сохраняем фамилию
		user = check_sign_in(request)
		if user.is_authenticated():
			user.last_name = request.POST['user']
			user.save()
		return JsonResponse({'success': True})
	else:
		raise Http404('Такая страница не существует')

@csrf_exempt
def search(request, page_number=1):
	if 'search' in request.session:
		login = check_sign_in(request)
		categories = Category.objects.all()
		data = request.session['search']
		args = {'login': login, 'categories': categories, 'tests_category': data.get('category','all'), 'url': '/tests/search/page/'}
		args.update(csrf(request))

		if request.method == 'POST':
			request.session['search']['text'] = request.POST.get('search','')

		#Проверка категории
		if data['category'] == 'all':
			tests = Test.objects.filter(public_access=True, title__icontains=data['text'])
			search_category_test = "Все"
		else:
			search_category_test = get_object_or_404(Category, url=data['category'])
			tests = Test.objects.filter(public_access=True, category=search_category_test, title__icontains=data['text'])
			
		
		args['search'] = {'text': data['text'], 'count': tests.count, 'category': search_category_test}
		current_page = Paginator(tests, 15)
		if int(page_number) > current_page.num_pages or int(page_number) < 1:
			raise Http404('Такой страницы нет')

		args['pages_count'] = get_number_name(current_page.num_pages + 2)
		args['tests'] = current_page.page(page_number)
		return render_to_response('tests.html', args)
	else:
		raise Http404('Что-то пошло не так')

@csrf_exempt
def test(request, id):
	login = check_sign_in(request)
	test = get_object_or_404(Test, id=id, public_access=True)
	if request.is_ajax():
		#Если не существует сессии с данным тестом , мы ее создаем
		if 'test' not in request.session or request.session['test']['id'] != test.id:
			questions = models_to_dict(Query.objects.filter(test=test).order_by('?')[:test.questions_count])
			random.shuffle(questions)

			request.session['test'] = {
				'id': test.id,
				'questions' : list(map(lambda quest: quest['id'], questions)),
				'answers' : [],
				'current_quset': 0,
				'user': ''
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

		#проверяем авторизирован ли пользователь и присутствие имении в сессии
		#Включаем возможность модификации сесии
		request.session.modified = True

		if login.is_authenticated() and len(login.get_full_name()) != 0:
			request.session['test']['user'] = login.get_full_name()
			name = True
		elif len(request.session['test']['user']) == 0:
			name = False

		return HttpResponse(json.dumps({'quest': quest, 'answers': answers, 'name': name}))
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
				for num in range(len(test_data['questions'])):
					question = Query.objects.get(id=test_data['questions'][num])
					test_data['questions'][num] = model_to_dict(question)
					max_points += test_data['questions'][num]['point']
					check_question = True
					#перебираем ответы и формируем ответ, так же полученный бал и максимально возможный балл
					for answer in test_data['answers'][num]:
						answer_data = model_to_dict(Answer.objects.get(id=answer['id'],query=question))
						if answer_data['correct'] != answer['selection']:
							check_question = False
							answer['error'] = True
						else:
							answer['error'] = False
						answer['correct'] = answer_data['correct']
						answer['text'] =  answer_data['text']
					if check_question:
						user_points += test_data['questions'][num]['point']

					test_data['questions'][num]['answers'] = test_data['answers'][num]

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
				user = check_sign_in(request)
				if user.is_authenticated():
					probationer = Probationer(
						test = Test.objects.get(id=test['id']),
						user = user,
						name = test_data['user'],
						precent = round(user_percent, 1),
						mark = result,
						date = datetime.datetime.now()
					)
				else:
					probationer = Probationer(
						test = Test.objects.get(id=test['id']),
						name = test_data['user'],
						precent = round(user_percent, 1),
						mark = result,
						date = datetime.datetime.now()
					)
				probationer.save()
				#удаляем сессию
				questions = test_data['questions']
				del request.session['test']

				return HttpResponse(json.dumps({'test_result': result, 'color': color, 'questions': questions}))
		else:
			raise Http404('Отсутствует сессия')
	else:
		raise Http404('Такая страница не существует!')