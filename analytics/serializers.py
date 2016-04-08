from rest_framework import serializers
from .models import Role, Specialization, Tested, Analytic

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization

class AnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytic
        fields = ('answer',)

class TestedSerializer(serializers.ModelSerializer):
    analytics = AnalyticSerializer(source='get_analytic', read_only=True, many=True)
    class Meta:
        model = Tested
        fields = ('id', 'role', 'course', 'specialization', 'date', 'test', 'analytics')