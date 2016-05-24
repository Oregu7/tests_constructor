from .models import Probationer, ProbationerAnswer
from constructor.serializers import OptionSerializer, OptionSecondSerializer, AnswerSerializer
from users.serializers import UserSerializer

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
