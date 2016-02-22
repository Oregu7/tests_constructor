from rest_framework import serializers
from constructor.models import Test, Query, Answer, Category
from tests.models import Probationer
from django.contrib.auth.models import User

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'title', 'description', 'category', 'two_mark', 'three_mark', 'four_mark')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'correct', 'query')

class QuerySerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(source='get_answers', read_only=True, many=True)
    class Meta:
        model = Query
        fields = ('id', 'text', 'point', 'answers', 'help', 'time', 'test')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'url')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class ProbationerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probationer
        fields = ('test', 'name', 'mark', 'percent')