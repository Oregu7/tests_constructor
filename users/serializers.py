from rest_framework.serializers import ModelSerializer
from .models import Specialization, Group, User
from constructor.serializers import CategorySerializer

class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization

class GroupSerializer(ModelSerializer):
    specialization = SpecializationSerializer()
    class Meta:
        model = Group

class UserSerializer(ModelSerializer):
    study_group = GroupSerializer()
    subjects = CategorySerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'study_group', 'is_staff', 'is_superuser', 'subjects')
