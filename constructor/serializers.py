from rest_framework import serializers
from constructor.models import Test, Query, Answer, Category

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'title', 'description', 'category', 'two_mark', 'three_mark', 'four_mark')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'correct')

class QuerySerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(source='get_answers', read_only=True, many=True)
    class Meta:
        model = Query
        fields = ('id', 'text', 'point', 'answers')
