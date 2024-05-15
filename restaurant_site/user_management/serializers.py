from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=6, style={'input_type': 'password'})
    class Meta:
        model = get_user_model()
        fields = ['emp_id', 'name', 'password']

    def create(self, validated_data):
        user_password = validated_data.get('password', None)
        db_instance = self.Meta.model(emp_id=validated_data.get('emp_id'), name=validated_data.get('name'))
        db_instance.set_password(user_password)
        db_instance.save()
        return db_instance
    
class UserLoginSerializer(serializers.Serializer):
    employee_id = serializers.CharField(min_length=4, max_length=4)
    password = serializers.CharField(max_length=100, min_length=6, style={'input_type': 'password'})
    token = serializers.CharField(max_length=255, read_only=True)