from django.shortcuts import render_to_response, redirect, get_object_or_404
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from testsConstructor.helpers import str_to_bool, get_number_name
from constructor.models import Test, Query, Answer, Category, Option
from .models import Probationer, ProbationerAnswer
from constructor.serializers import TestSerializer, QuerySerializer, CategorySerializer, TestSecondSerializer
from tests.models import Probationer
from django.utils import timezone
import json
import random
import datetime
# Create your views here.

@login_required
def tests(request):
    user = request.user
    if request.is_ajax():
        if request.method == "GET":
            tests = TestSerializer(Test.objects.filter(group_access=user.study_group), many=True).data
            categories = [{'name': 'Все', 'url': ''}]
            for test in tests:
                if test['category'] not in categories:
                    categories.append(test['category'])

            return JsonResponse({'tests': tests, 'categories': categories})
    else:
        data = {'login': user}
        data.update(csrf(request))
        return render_to_response('tests_main.html', data)

@login_required
def get_page(request, name):
    return render_to_response(name + '.html')

@login_required
def test_detail(request, id):
    user = request.user
    test = get_object_or_404(Test, id=id, group_access=user.study_group)

    if request.method == "GET":
        test_serializer = TestSecondSerializer(test).data
        return JsonResponse({'test': test_serializer})
    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        option = get_object_or_404(Option, id=data.get('option', ''), test=test)
        probationer = Probationer(
            option = option,
            user = user,
            mark = data.get('mark', ''),
            precent = round(data.get('percent', ''), 2),
            date = timezone.now()
        )

        probationer.save()
        for question in data.get('questions', ''):
            for answer in question['answers']:
                if answer.get('selected', False):
                    answer = get_object_or_404(Answer, id=answer['id'])
                    probationer_answer = ProbationerAnswer(
                        probationer = probationer,
                        answer = answer
                    )

                    probationer_answer.save()

        return HttpResponse(status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)