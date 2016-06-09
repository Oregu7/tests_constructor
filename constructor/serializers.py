from rest_framework import serializers
from constructor.models import Test, Query, Answer, Category, Option
from tests.models import Probationer
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'url')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'correct', 'query', 'analytics')

class QuerySerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(source='get_answers', read_only=True, many=True)
    class Meta:
        model = Query
        fields = ('id', 'text', 'point', 'answers', 'help', 'test')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class ProbationerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probationer
        fields = ('test', 'name', 'mark', 'percent')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ('text', 'id', 'point')

class OptionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True)
    class Meta:
        model = Option

class OptionSecondSerializer(serializers.ModelSerializer):
    questions = QuerySerializer(read_only=True, many=True)
    class Meta:
        model = Option

class OptionThreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'number')

class TestSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Test
        fields = (
            'id',
            'title',
            'description',
            'category',
            'two_mark',
            'three_mark',
            'four_mark',
            'time_completion',
            'helps',
        )

class TestSecondSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    options = OptionSecondSerializer(read_only=True, source="get_options", many="True")
    class Meta:
        model = Test
        fields = (
            'id',
            'title',
            'description',
            'category',
            'two_mark',
            'three_mark',
            'four_mark',
            'time_completion',
            'helps',
            'options'
        )

