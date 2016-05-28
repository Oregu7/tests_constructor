from .models import Probationer, ProbationerAnswer
from constructor.serializers import OptionSerializer, OptionSecondSerializer, AnswerSerializer, CategorySerializer
from users.serializers import UserSerializer
from constructor.models import Test, Option
from rest_framework.serializers import ModelSerializer


class ProbationerAnswersSerializer(ModelSerializer):
    answer = AnswerSerializer()
    class Meta:
        model = ProbationerAnswer

class ProbationerSerializer(ModelSerializer):
    option = OptionSecondSerializer()
    user = UserSerializer()
    answers = ProbationerAnswersSerializer(source="get_answers", read_only=True, many=True)
    class Meta:
        model = Probationer
        fields = ('id', 'user', 'mark', 'precent', 'date', 'answers', 'option')

class TestProbSer(ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Test
        fields = ('title', 'category')

class OptionProbSer(ModelSerializer):
    test = TestProbSer()
    class Meta:
        model = Option
        fields = ('number', 'test')

class ProbationerSecondSerializer(ModelSerializer):
    option = OptionProbSer()
    class Meta:
        model = Probationer
        fields = ('id', 'mark', 'precent', 'date', 'option')