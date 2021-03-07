from rest_framework import serializers, status, viewsets , filters
from rest_framework.decorators import action, permission_classes
from account.models import User
from account.serializer import UserListSerializer, UserSerializer, UserUpdateSerializer
from helper import getPositiveResponse ,getNegativeResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from account.authentication import CustomAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from djongo.models import Q

class UserProfileViewSet(viewsets.ViewSet):
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)

    @action(detail=False, methods=["GET"])
    def userlist(self, request):
        try:
            user = self.request.user
            if user:
                user = User.objects.all()
                serializer = UserListSerializer(user, many=True)
                data = getPositiveResponse(
                    "User list", serializer.data)
                return Response(data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["GET"])
    def search(self, request):
        try:
            user = self.request.user
            if user:
                search_user = User.objects.all()
                query = self.request.query_params.get('q',None)
                if query is not None:
                    search= search_user.filter(Q(username__icontains=query)|Q(email__icontains=query))
                serializer = UserListSerializer(search, many=True)
                data = getPositiveResponse("search_user", serializer.data)
                return Response(data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    def retrieve(self, request, pk=None):
        try:
            user = self.request.user
            if user:
                user = User.objects.get(pk=pk)
                serializer = UserListSerializer(user)
                data = getPositiveResponse("search_user", serializer.data)
                return Response(data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)
