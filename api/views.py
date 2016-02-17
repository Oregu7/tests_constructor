from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from constructor.models import Test, Category, Answer, Query
from constructor.serializers import TestSerializer, AnswerSerializer, QuerySerializer

# Create your views here.
@api_view(['GET'])
def test_list(request):
    if request.method == 'GET':
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
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

@api_view(['GET'])
def question_list(request, id):
    try:
        test = Test.objects.get(id=id)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        questions = Query.objects.filter(test=test)
        serializer = QuerySerializer(questions, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

