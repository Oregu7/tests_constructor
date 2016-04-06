from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, JsonResponse, QueryDict, Http404
from django.views.decorators.csrf import csrf_exempt
from constructor.models import Query, Answer, Test
from .models import Role, Specialization, Tested, Analytic
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
        file_name = u"test#%s_answers" % test.id
        serializer = list(map(change_answers, serializer.data))
        return make_response_from_records(serializer, 'xls', file_name=file_name)
    elif data == "questions":
        questions = Query.objects.filter(test=test)
        file_name = u'test#%s_questions' % test.id
        column_names = ['id', 'text']
        return make_response_from_query_sets(questions, column_names, 'xls', file_name=file_name)
    else:
        return Http404("Does Not Exist")

def change_answers(answer):
    response = {
        'ID_Вопроса': answer['query'],
        'Текст_Ответа': answer['text'],
        'Аналитика': answer['analytics']
    }

    return response