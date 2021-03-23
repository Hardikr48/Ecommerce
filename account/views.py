import threading
from .models import User
from .serializer import UserSerializer ,ForgotPasswordSerializer
from .authentication import CustomAuthentication
from rest_framework import serializers, status, viewsets 
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.messages import constants
from  helper import getPositiveResponse ,getNegativeResponse
from django.db.models import Q
from rest_framework_jwt.settings import api_settings
from account.serializer import LoginSerializer, ResetPasswordSerializer, UserListSerializer, UserPasswordUpdateSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from account.models import BlackList, UserAccessToken, UserVerification
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import  AllowAny
from ecommerce import settings
from rest_framework.exceptions import ValidationError
import random
import string
import traceback
import datetime


class UserViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["post"])
    def signup(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            response = getPositiveResponse(
                "Add User", serializer.data)
            return Response(response)    
        else:
            data = getNegativeResponse("category is not valid")
            return Response(data)

    @action(detail=False, methods=["post"])
    def changepassword(self,request):
        response = {}
        try:
            user = self.request.user
            if user:
                passward_ser = UserPasswordUpdateSerializer(data=request.data)
                if passward_ser.is_valid() == False:
                    response = getNegativeResponse(
                        "enter password")
                    return Response(response)
                password_data = passward_ser.validated_data
            
                if user.check_password(password_data['password']) == True:
                    user.set_password(password_data['new_password'])
                    user.save()
                else:
                    return Response('Old password is not valid.')

                response = getPositiveResponse(
                    "Password updated successfully")
                return Response(response)
        except User.DoesNotExist:
            response = getNegativeResponse("User Not Valid ")
            return Response(response)

    permission_classes = (AllowAny,)
    @action(detail=False, methods=["post"])
    def forgotpassword(self,request):
        response = {}
        forgot_password_ser = ForgotPasswordSerializer(data=request.data)
        if forgot_password_ser.is_valid() == False:
            response = getNegativeResponse(
                    "enter password")
            return Response(response)
        try:
            data = forgot_password_ser.data
            data['email'] = data['email'].lower()
            forgot_password_ser = ForgotPasswordSerializer(
                User.objects.get(email=data['email']), data=data)
            forgot_password_ser.is_valid(raise_exception=True)
            user = forgot_password_ser.save()
            response = getPositiveResponse(
                    "Password Link Sent at your email")
            return Response(response)
        except User.DoesNotExist:
            response = getNegativeResponse("No user found with email ")
            return Response(response)

    permission_classes = (AllowAny,)
    @action(detail=False, methods=["post"])
    def forgotpasswordupdate(self, request):
        response = {}
        reset_password_ser = ResetPasswordSerializer(data=request.data)
        
        if reset_password_ser.is_valid() == False:
            response = self.getErrorMessage(
                reset_password_ser, status.HTTP_400_BAD_REQUEST)
            return Response(response, status=response['statusCode'])

        try:
            unique_token = reset_password_ser.data['reset_password_token']
            BlackList.objects.get(token=unique_token)
            raise ValidationError('Unauthorized TOKEN')

        except BlackList.DoesNotExist:
                pass
        try:
            user = UserVerification.objects.get(verification_token=unique_token)
            now = datetime.datetime.now()
            now_plus = user.created + datetime.timedelta(minutes = 5)
            current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            token_time = now_plus.strftime("%m/%d/%Y, %H:%M:%S")

            if token_time  >= current_time:
                user = UserVerification.objects.get(verification_token=unique_token)
                user = User.objects.get(id=user.id)
                user.set_password(reset_password_ser.data['password'])
                user.save()
                black_list_token = BlackList(token=unique_token)
                black_list_token.save()
                return Response("password is update")
            else:
                data = getNegativeResponse("token is expire")
                return Response(data)
        except UserVerification.DoesNotExist:
            return Response("password is not update")
        