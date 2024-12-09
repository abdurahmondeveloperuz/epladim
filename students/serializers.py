from rest_framework import serializers
from .models import Student, Class

class StudentSerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'score', 'rank']