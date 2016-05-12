from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, JsonResponse, QueryDict, Http404
from django.views.decorators.csrf import csrf_exempt
from constructor.models import Query, Answer, Test
from .models import Role, Specialization, Tested, Analytic
from .serializers import TestedSerializer, AnalyticSerializer
from constructor.serializers import QuerySerializer, AnswerSerializer
from django_excel import make_response_from_query_sets, make_response_from_records, make_response_from_book_dict
import json
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import io
from xlsxwriter.workbook import Workbook

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
    specialization = get_object_or_404(Specialization, code=tested['specialization'])
    tested_new = Tested(
        role = role,
        specialization = specialization,
        course = tested['course'],
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
        return make_response_from_query_sets(questions, column_names, 'xlsx', file_name=file_name)
    elif data == "testeds":
        testeds = change_testeds(TestedSerializer(Tested.objects.filter(test=test), many=True).data)
        file_name = u'test#%s_testeds' % str(test.id)
        return make_response_from_records(testeds, 'xls', file_name=file_name)
    else:
        return Http404("Does Not Exist")

def change_answers(answer):
    response = {
        'ID_Вопроса': answer['query'],
        'ID_Ответа': answer['id'],
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
    if value != "all":
        mapping[key] = value

def inc_answer(mapping, id):
    def find_by_id(answer):
        if answer['id'] == id:
            answer['analytics'] += 1
        return answer

    mapping = list(map(find_by_id, mapping))

def search_and_send_to_excel(request, data, test, role, spec, course, date_f, date_l):
    sort_params = {}
    set_if_not_none(sort_params, 'test', test)
    set_if_not_none(sort_params, 'role', role)
    set_if_not_none(sort_params, 'specialization', spec)
    set_if_not_none(sort_params, 'course', course)

    if date_f != "all" and date_l != "all":
        sort_params['date__range'] = (date_f, date_l)

    testeds = Tested.objects.filter(**sort_params)
    testeds_serializer = TestedSerializer(testeds, many=True)
    if data == "answers":
        answers = Answer.objects.filter(query__test=test)
        answers_data = AnswerSerializer(answers, many=True).data

        for tested in testeds_serializer.data:
            for analytic in tested['analytics']:
                inc_answer(answers_data, analytic['answer'])

        file_name = u"test#%s_answers" % str(test)
        excel_data = list(map(change_answers, answers_data))
        return make_response_from_records(excel_data, 'xlsx', file_name=file_name)

    elif data == "testeds":
        testeds = change_testeds(testeds_serializer.data)
        file_name = u'test#%s_testeds' % str(test)
        return make_response_from_records(testeds, 'xlsx', file_name=file_name)

    elif data == "testeds_answers":
        output = io.BytesIO()
        testeds_answers = AnalyticSerializer(Analytic.objects.filter(tested__in = testeds), many=True).data
        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('ответы_тестируемых')
        for indx in range(len(testeds_answers)):
            worksheet.write("A%s" % str(indx + 2), testeds_answers[indx]['tested'])
            worksheet.write("B%s" % str(indx + 2), testeds_answers[indx]['answer'])

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=test.xlsx"
        return response

        #file_name = u'test#%s_testeds_answers' % str(test)
        #return make_response_from_records(testeds_answers.data, 'xlsx', file_name=file_name)
    else:
        return Http404("Does Not Exist")