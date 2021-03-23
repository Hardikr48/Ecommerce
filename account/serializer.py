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

class UserVerificationSerializer(serializers.Serializer):
    verification_type = serializers.CharField(required=False)
    verification_token = serializers.CharField(required=False)
    user = serializers.CharField(required=False)
    class Meta:
        model = UserVerification
        fields = ('user','verification_type', 'verification_token','user')

    def create(self, validated_data):
        user_verification = None
        verification_type = UserVerification.USER_VERIFICATION_TYPES[0][0]

        if 'verification_type' in validated_data:
            verification_type = validated_data['verification_type']
        user = User.objects.get(id=validated_data['user'])
    
        user_verifications = UserVerification.objects.filter(user=user)
    

        if user_verifications.count() > 0:
            user_verification = user_verifications[0]
            user_verification.verification_token = validated_data['verification_token']
        else: 
            user_verification = UserVerification(
                user=user,
                verification_type=verification_type,
                verification_token=validated_data['verification_token']
            )
        user_verification.save()
        return user_verification

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False, error_messages={
        'required': 'Please enter a valid email address.',
        'invalid': 'Please enter a valid email address.',
        'blank': 'Email address may not be blank'
    })

    class Meta:
        model = User
        fields = ('email')

    def update(self, instance, validated_data):
        verification_token = ""
        is_unique = False
        while is_unique != True:
            verification_token = randomGeneratorCode()
            try:
                UserVerification.objects.get(
                    verification_token=verification_token)
            except UserVerification.DoesNotExist:
                is_unique = True


        try:
            
            user = User.objects.get(id=validated_data['user'])
            user_verifications = UserVerification.objects.filter(user=user)
            user_verification_serializer = UserVerificationSerializer(UserVerification.objects.get(
                user=user,verification_type=UserVerification.USER_VERIFICATION_TYPES[
                    1][0]
            ),
                data={'user': instance.id, 'verification_token': verification_token})
        except:
            data={'user': instance.id,
                'verification_type': UserVerification.USER_VERIFICATION_TYPES[1][0],
                'verification_token': verification_token
                }
            print(data)    
            user_verification_serializer = UserVerificationSerializer(data={'user': instance.id,
                                                                            'verification_type': UserVerification.USER_VERIFICATION_TYPES[1][0],
                                                                            'verification_token': verification_token
                                                                            }
                                                                      )

        user_verification_serializer.is_valid(raise_exception=True)
        user_verification = user_verification_serializer.save()
        user_verification.created=datetime.datetime.now()
        user_verification.save()
        from_email = settings.EMAIL_HOST_USER
        to_email = validated_data['email']
        recipient = [to_email]
        send_mail("message",verification_token, from_email,recipient,fail_silently = False)

        return instance