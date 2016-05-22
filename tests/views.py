from django.shortcuts import render_to_response, redirect, get_object_or_404
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from django.forms.models import model_to_dict
from testsConstructor.helpers import str_to_bool, get_number_name
from constructor.models import Test, Query, Answer, Category
from constructor.serializers import TestSerializer, QuerySerializer, CategorySerializer, TestSecondSerializer
from tests.models import Probationer
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
    if request.method == "GET":
        user = request.user
        test = get_object_or_404(Test, id=id, group_access=user.study_group)
        test_serializer = TestSecondSerializer(test).data
        return JsonResponse({'test': test_serializer})
    else:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)