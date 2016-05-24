from rest_framework.serializers import ModelSerializer
from .models import Specialization, Group, User

class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization

class GroupSerializer(ModelSerializer):
    specialization = SpecializationSerializer()
    class Meta:
        model = Group

class UserSerializer(ModelSerializer):
    study_group = GroupSerializer()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'study_group')
