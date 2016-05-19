from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from testsConstructor.helpers import check_sign_in, str_to_bool, put
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from django.forms.models import model_to_dict
from .models import Test, Query, Answer, Category, Option
from .serializers import OptionSerializer, QuestionSerializer
from users.models import Specialization, Group
from users.serializers import SpecializationSerializer, GroupSerializer
from django.contrib import auth
from rest_framework import status
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

@csrf_exempt
def create_test(request):
    login = check_sign_in(request)
    if login:
        if request.is_ajax():
            category = get_object_or_404(Category,id=int(request.POST['category']))

            test = Test(
                title = request.POST['title'],
                description = request.POST['description'],
                helps = str_to_bool(request.POST['helps']),
                time_completion = str_to_bool(request.POST['timeCompl']),
                creator = auth.get_user(request),
                category = category,
                questions_count = request.POST['quest_count'],
                two_mark = request.POST['two_mark'],
                three_mark = request.POST['three_mark'],
                four_mark = request.POST['four_mark']
            )
            test.save()

            return JsonResponse({'testID': test.id, 'error': False})
        else:
            categories = Category.objects.all()
            return render_to_response('create_test.html', {'login': login, 'categories': categories})
    else:
        return redirect('/')

@csrf_exempt
def settings_test(request, id):
    test = get_object_or_404(Test, id=id)
    if test.creator == auth.get_user(request):
        if request.is_ajax():
            category = get_object_or_404(Category,id=int(request.POST['category']))

            test.title = request.POST['title']
            test.description = request.POST['description']
            test.helps = str_to_bool(request.POST['helps'])
            test.time_completion = request.POST['timeCompl']
            test.two_mark = request.POST['two_mark']
            test.three_mark = request.POST['three_mark']
            test.four_mark = request.POST['four_mark']
            test.category = category
            test.questions_count = request.POST['quest_count']
            test.save()

            return JsonResponse({'success': 'Данные сохранены!'})
        else:
            login = check_sign_in(request)
            categories = Category.objects.all()
            return render_to_response('create_test.html', {'login': login, 'test': test, 'categories': categories, 'optionName': 'settings'})
    else:
        return redirect('/')

@csrf_exempt
def queries_test(request, id):
    sign_in = check_sign_in(request)
    test = get_object_or_404(Test, id=id)
    if test.creator == auth.get_user(request):
        queries = map(get_answers, Query.objects.filter(test = test))
        return render_to_response('test/queries.html', {'login': sign_in, 'test': test, 'queries': queries, 'optionName': 'questions'})
    else:
        raise Http404('Вы не являетесь создателем данного теста!')

@csrf_exempt
def add_query(request, id):
    test = get_object_or_404(Test, id=int(id))
    user = auth.get_user(request)
    if test.creator == user:
        #кодим тут (когда все True)
        if request.is_ajax():
            query = Query(
                test = test,
                text = request.POST['text'],
                point = request.POST['point'],
                help = request.POST['help']
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
            return render_to_response('add_query.html', {'login': user, 'test': test})
    else:
        raise Http404('Вы не являетесь создателем данного теста!')

@csrf_exempt
def delete_query(request, t_id, q_id):
    test = get_object_or_404(Test, id = t_id)
    if test.creator == auth.get_user(request):
        question = get_object_or_404(Query, test=test, id=q_id)
        question.delete()
        return redirect('/constructor/test/' + t_id + '/questions/')
    else:
        raise Http404('Вы не являетесь создателем данного теста!')

@csrf_exempt
def edit_question(request, t_id, q_id):
    test = get_object_or_404(Test, id=t_id)
    question = get_object_or_404(Query, id=q_id)
    login = check_sign_in(request)

    if test.creator == auth.get_user(request):
        if request.method == 'POST':
            #отправляем model
            return HttpResponse(json.dumps(model_to_dict(question)))
        elif request.method == 'PUT':
            #парсим put запрос
            data = put(request)
            #обновляем данные
            question.help = data.get('help')
            question.point = int(data.get('point'))
            question.text = data.get('text')
            question.save()

            return HttpResponse(json.dumps(data))
        elif request.method == 'GET':
            return render_to_response('add_query.html',
                {
                    'login': login,
                    'test': test,
                    'question': question
                }
            )
    else:
        return Http404('Вы не являетесь создателем данного теста!')

@csrf_exempt
def question_actions(request, qid, aid):
    question = get_object_or_404(Query, id=qid)
    if question.test.creator == auth.get_user(request):
        if request.method == 'DELETE':
            answer = get_object_or_404(Answer, query=qid, id=aid)
            answer.delete()
            return JsonResponse({'msg':'delete'})
        elif request.method == 'PUT':
            answer = get_object_or_404(Answer, query=qid, id=aid)
            #парсим put запрос
            data = put(request)
            #обновляем данные
            answer.text = data.get('text')
            answer.correct = data.get('correct')
            answer.save()

            return JsonResponse({'msg':'success'})
        elif request.method == 'POST':
            question = get_object_or_404(Query, id=qid)
            answer = Answer(query=question)

            answer.save()
            return JsonResponse({'id': answer.id})

        #достаем коллекцию овтетов данного вопроса
        elif request.method == 'GET':
            question = get_object_or_404(Query, id=qid)
            answers = Answer.objects.filter(query=question)
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
        return Http404('Вы не являетесь создателем данного теста!')

@csrf_exempt
def test_access(request, id):
    test = get_object_or_404(Test, id=id)
    login = check_sign_in(request)
    if test.creator == login:
        if request.is_ajax():
            #Формируем данные
            if request.method == 'GET':
                specializations = SpecializationSerializer(Specialization.objects.all(), many=True).data
                groups_access = GroupSerializer(test.group_access.all(), many=True).data
                groups = GroupSerializer(Group.objects.all().order_by('course','name'), many=True).data
                for group in groups:
                    if group in groups_access:
                        group['access'] = True
                    else:
                        group['access'] = False
                courses = list(map(lambda x: {'id': x, 'name': str(x)}, range(1, 5)))
                return JsonResponse({'specs': specializations, 'groups': groups, 'courses': courses})
            elif request.method == 'POST':
                group = get_object_or_404(Group, id=request.POST.get('group', ''))
                if str_to_bool(request.POST.get('append', False)):
                    test.group_access.add(group)
                else:
                    test.group_access.remove(group)
                return JsonResponse({'success': True})
            elif request.method == "DELETE":
                test.group_access.clear()
                return JsonResponse({'success': True})
        else:
            return render_to_response('test_access.html',{'login': login, 'test': test, 'optionName': 'access'})
    else:
        return Http404('Вы не имете доступа!')

#@api_view(['GET', 'POST', 'DELETE'])
def test_options(request, id):
    test = get_object_or_404(Test, id=id)
    user = check_sign_in(request)
    if test.creator == user:
        if request.is_ajax():
            if request.method == 'GET':
                questions = QuestionSerializer(Query.objects.filter(test=test), many=True).data
                options = OptionSerializer(Option.objects.filter(test=test), many=True).data
                return JsonResponse({'questions': questions, 'options': options})
            if request.method == 'POST':
                data = json.loads(request.body.decode("utf-8"))
                #добавление варианта
                if data.get('action', '') == "addOption":
                    option = Option(
                        test = test,
                        number = data.get('number', 1)
                    )
                    option.save()
                    return JsonResponse({'id': option.id})
                #действие не инициализированно
                else:
                    return JsonResponse({'error': 'Action Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            data = {'test': test, 'login': user, 'optionName': 'options'}
            data.update(csrf(request))
            return render_to_response('test_options.html', data)
    else:
        return Http404('Вы не имете доступа!')