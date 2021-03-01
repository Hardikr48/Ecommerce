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

