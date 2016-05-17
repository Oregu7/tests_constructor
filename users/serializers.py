from rest_framework.serializers import ModelSerializer
from .models import Specialization, Group, User

class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
