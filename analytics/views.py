from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, JsonResponse, QueryDict, Http404
from django.views.decorators.csrf import csrf_exempt
from constructor.models import Query, Answer, Test
from .models import Role, Specialization, Tested, Analytic
from .serializers import TestedSerializer, AnalyticSerializer
from constructor.serializers import QuerySerializer, AnswerSerializer
from django_excel import make_response_from_query_sets, make_response_from_records
import json
import pyexcel.ext.xls

def index(request):
    return render_to_response('analytics.html')

def get_page(request, page):
    return render_to_response(page)

@csrf_exempt
def save_analytics(request):
    print(request.POST)
    data = json.loads(request.POST['data'])
    tested = json.loads(request.POST['tested'])

    role = get_object_or_404(Role, id=tested['role'])
    test = get_object_or_404(Test, id=request.POST['test'])

    #если тестируемый студент
    if role.id == 1:
        specialization = get_object_or_404(Specialization, code=tested['specialization'])
        tested_new = Tested(
            role = role,
            specialization = specialization,
            course = tested['course'],
            test = test
        )
        tested_new.save()
    else:
        tested_new = Tested(
            role = role,
            test = test
        )
        tested_new.save()

    for analytic in data:
        if analytic['current_answer']:
            answer = Answer.objects.get(id=analytic['current_answer'], query__id=analytic['id'])
            analytic_new = Analytic(
                answer = answer,
                tested = tested_new
            )

            analytic_new.save()

    return JsonResponse({'success': True})

def send_to_excel(request, data, test):
    test = get_object_or_404(Test, id=test)

    if data == "answers":
        answers = Answer.objects.filter(query__test=test)
        serializer = AnswerSerializer(answers, many=True)
        file_name = u"test#%s_answers" % str(test.id)
        serializer = list(map(change_answers, serializer.data))
        return make_response_from_records(serializer, 'xls', file_name=file_name)
    elif data == "questions":
        questions = Query.objects.filter(test=test)
        file_name = u'test#%s_questions' % str(test.id)
        column_names = ['id', 'text']
        return make_response_from_query_sets(questions, column_names, 'xls', file_name=file_name)
    elif data == "testeds":
        testeds = change_testeds(TestedSerializer(Tested.objects.filter(test=test), many=True).data)
        file_name = u'test#%s_testeds' % str(test.id)
        return make_response_from_records(testeds, 'xls', file_name=file_name)
    else:
        return Http404("Does Not Exist")

def change_answers(answer):
    response = {
        'ID_Вопроса': answer['query'],
        'Текст_Ответа': answer['text'],
        'Аналитика': answer['analytics']
    }

    return response

def change_testeds(testeds):
    for tested in testeds:
        tested['count_answers'] = len(tested['analytics'])
        del tested['analytics']
        del tested['test']

    return testeds

def set_if_not_none(mapping, key, value):
    if value is not "":
        if key == 'specialization' or key == 'course':
            if 'role' in mapping and mapping['role'] is "1":
                mapping[key] = value
        else:
            mapping[key] = value

def inc_answer(mapping, id):
    def find_by_id(answer):
        if answer['id'] == id:
            answer['analytics'] += 1
        return answer

    mapping = list(map(find_by_id, mapping))

def search_and_send_to_excel(request, test, role, spec, course, date_f, date_l):
    sort_params = {}
    set_if_not_none(sort_params, 'test', test)
    set_if_not_none(sort_params, 'role', role)
    set_if_not_none(sort_params, 'specialization', spec)
    set_if_not_none(sort_params, 'course', course)

    if date_f is not "" and date_l is not "":
        sort_params['date__range'] = (date_f, date_l)

    testeds = Tested.objects.filter(**sort_params)
    testeds_serializer = TestedSerializer(testeds, many=True)
    answers = Answer.objects.filter(query__test=test)
    answers_data = AnswerSerializer(answers, many=True).data

    for tested in testeds_serializer.data:
        for analytic in tested['analytics']:
            inc_answer(answers_data, analytic['answer'])

    file_name = u"test#%s_answers" % test
    excel_data = list(map(change_answers, answers_data))
    return make_response_from_records(excel_data, 'xls', file_name=file_name)