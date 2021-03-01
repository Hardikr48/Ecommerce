from .models import User 
from rest_framework import serializers
from account.models import UserVerification
from ecommerce import settings
from django.core.mail import send_mail
from helper import randomGeneratorCode
import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","first_name", "last_name" ,"mobile_number","email","username","password","address","city","state","zipcode")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","first_name", "last_name" ,"mobile_number","email","username","address","city","state","zipcode")

class ResetPasswordSerializer(serializers.Serializer):
    reset_password_token = serializers.CharField(max_length=255, required=True, error_messages={
        'required': 'Please enter a reset password token.',
        'blank': 'Reset password token may not be blank'
    })
    password = serializers.CharField(min_length=5, max_length=35, required=True, error_messages={
        'required': 'Please enter a password.',
        'blank': 'Password may not be blank'
    })

    class Meta:
        model = UserVerification
        fields = ('reset_password_token', 'password')

    def update(self, instance, validated_data):
        user_verification = instance
        user_verification.user.set_password(validated_data['password'])
        user_verification.user.save()
        user_verification.save()
        return user_verification


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","first_name", "last_name" ,"mobile_number","email","username","address","city","state","zipcode")

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={
        'required': 'Please enter a valid email address.',
        'invalid': 'Please enter a valid email address.',
        'blank': 'Email address may not be blank'
    })
    password = serializers.CharField(
        max_length=50, allow_blank=True, required=False, default="")
    fcm_token = serializers.CharField(
        min_length=5, required=False, allow_blank=True, default="")

class UserPasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=5, max_length=35, allow_blank=False, required=True, error_messages={
        'required': 'Please confirm your password.',
        'blank': 'New password may not be blank'
    })
    password = serializers.CharField(min_length=5, max_length=35, allow_blank=False, required=True, error_messages={
        'required': 'Please enter a password.',
        'blank': 'Password may not be blank'
    })

