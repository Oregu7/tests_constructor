from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from testsConstructor.helpers import check_sign_in
from constructor.models import Answer, Query, Test
from constructor.serializers import QuerySerializer, AnswerSerializer
from django.contrib.auth.decorators import login_required

import pyexcel.ext.xls
from django_excel import make_response_from_query_sets
from django_excel import make_response_from_array, make_response_from_records
from users.models import Group
from django.db.models import F

@login_required
def home(request):
    sign_in = check_sign_in(request)
    return redirect('/profile/')

def excel(request):
    test = Test.objects.get(id=1)
    answers = Answer.objects.filter(query__test=test)
    serializer = AnswerSerializer(answers, many=True)
    file_name = test.title + "_analytic"
    serializer = list(map(change_answers, serializer.data))

    return make_response_from_records(serializer, 'xls', file_name=file_name)

def change_answers(answer):
    response = {
        'ID_Вопроса': answer['query'],
        'Текст_Ответа': answer['text'],
        'Аналитика': answer['analytics']
    }

    return response