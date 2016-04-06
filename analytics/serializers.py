from rest_framework import serializers
from .models import Role, Specialization, Tested, Analytic

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization