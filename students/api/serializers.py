from rest_framework import serializers
import base64
import binascii

class StudentInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    score = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0, max_value=100)
    image = serializers.CharField(required=False, allow_blank=True)
    profile_url = serializers.URLField(required=False, allow_blank=True)

    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Score must be between 0 and 100")
        return value

    def validate_image(self, value):
        if value:
            try:
                # Check if the image is valid base64
                # base64.b64decode(value)
                pass
            except binascii.Error:
                raise serializers.ValidationError("Invalid base64 image data")
        return value

class ClassInputSerializer(serializers.Serializer):
    class_name = serializers.CharField(max_length=100)
    students = StudentInputSerializer(many=True)

    def validate_students(self, value):
        if not value:
            raise serializers.ValidationError("At least one student is required")
        return value

class StudentSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    score = serializers.DecimalField(max_digits=5, decimal_places=2)
    rank = serializers.IntegerField(required=False)
    image = serializers.CharField(required=False)
    profile_url = serializers.URLField(required=False)