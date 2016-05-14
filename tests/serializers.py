from .models import Probationer, ProbationerAnswers
from rest_framework.serializers import ModelSerializer


class ProbationerAnswersSerializer(ModelSerializer):
    class Meta:
        model = ProbationerAnswers

class ProbationerSerializer(ModelSerializer):
    answers = ProbationerAnswersSerializer(source="get_answers", read_only=True, many=True)
    class Meta:
        model = Probationer
        fields = ('id', 'test', 'user', 'mark', 'precent', 'date', 'answers')
