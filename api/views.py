from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404
from constructor.models import Test, Category, Answer, Query
from tests.models import Probationer
from django.contrib import auth
from django.contrib.auth.models import User
from constructor.serializers import TestSerializer, AnswerSerializer, QuerySerializer, CategorySerializer, UserSerializer, ProbationerSerializer
import datetime

# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST'])
def test_list(request):
    if request.method == 'GET':
        tests = Test.objects.filter(public_access=True)
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        user = User.objects.get(id=request.data['user'])
        category = Category.objects.get(url=request.data['category'])
        test = Test(
            title = request.data['title'],
            description = request.data['desc'],
            helps = request.data['helps'],
            time_completion = request.data['time'],
            creator = user,
            category = category,
            questions_count = request.data['count_questions'],
            two_mark = request.data['two_mark']['last'],
            three_mark = request.data['three_mark']['last'],
            four_mark = request.data['four_mark']['last']
        )

        test.save()
        serializer = TestSerializer(test)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def test_category(requset, category):
    try:
        category = Category.objects.get(url=category)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if requset.method == 'GET':
        tests = Test.objects.filter(category=category)
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def test_detail(request, id):
    try:
        test = Test.objects.get(id=id)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestSerializer(test)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def question_list(request, id):
    try:
        test = Test.objects.get(id=id)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        questions = Query.objects.filter(test=test)
        serializer = QuerySerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        question = QuerySerializer(data=request.data)
        if question.is_valid():
            question.save()
            for answer in request.data['answers']:
                answer['query'] = question.data['id']
                answer_ser = AnswerSerializer(data=answer)
                if answer_ser.is_valid():
                    answer_ser.save()
                else:
                    return Response(answer_ser.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer = QuerySerializer(Query.objects.get(id=question.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(question.errors, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET', 'POST'])
def user_detail(request):
    user = auth.authenticate(username=request.data['login'], password=request.data['password'])
    if user is not None:
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
def probationers_list(request):
    test = Test.objects.get(id=request.data['test'])
    probationer = Probationer(
        date = datetime.datetime.now(),
        test = test,
        name = request.data['name'],
        precent = round(request.data['percent'],2),
        mark = request.data['mark']
    )
    probationer.save()
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def question_detail(request, test_id, quest_id):
    if request.method == 'DELETE':
        test = get_object_or_404(Test, id=test_id)
        question = get_object_or_404(Query, id=quest_id, test=test)
        question.delete()
        return Response(status=status.HTTP_200_OK)
    if request.method == 'PUT':
        pass