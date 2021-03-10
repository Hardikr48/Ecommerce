from .models import Category
from .serializer import CategorySerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from account.authentication import CustomAuthentication
from rest_framework.permissions import IsAuthenticated
from helper import getNegativeResponse, getPositiveResponse


class CategoryViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)

    @action(detail=False, methods=["GET"])
    def categorylist(self, request):
        try:
            user = self.request.user
            if user:
                queryset = Category.objects.all()
                serializer = CategorySerializer(queryset, many=True)
                data = getPositiveResponse(
                    "List Of Category", serializer.data)
                return Response(data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["post"])
    def search(self, request):
        try:
            user = self.request.user
            if user:
                try:
                    category = Category.objects.filter(name__startswith=request.data['name']) 
                except Exception:
                    data = getNegativeResponse("invalid category")
                    return Response(data)
                serializer = CategorySerializer(category , many= True)
                data = getPositiveResponse("category", serializer.data)
                return Response(data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["post"])
    def delete(self, request):
        try:
            user = self.request.user
            if user:
                try:
                    category = Category.objects.get(id=request.data['id'])
                except Exception:
                    data = getNegativeResponse("invalid category")
                    return Response(data)
                operation = category.delete()
                data={}
                if operation:
                    data["success"] = "delete successful"
                    response = getPositiveResponse("category", data)
                    return Response(response)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["post"])
    def add(self, request):
        try:
            user = self.request.user
            if user:
                try:
                    category = Category.objects.get(id=request.data['id'])
                except Exception:
                    data = getNegativeResponse("invalid category")
                    return Response(data)
                serializer = CategorySerializer(data=request.data)
                if(serializer.is_valid()):
                    serializer.save()
                    response = getPositiveResponse(
                        "Add Category", serializer.data)
                    return Response(response)
                else:
                    data = getNegativeResponse("serializer is not valid")
                    return Response(data) 
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["post"])
    def categoryupdate(self,request,pk=None):
        try:
            user = self.request.user
            
            if user:
                try:
                    category = Category.objects.get(id=request.data['id'])
                except Exception:
                    data = getNegativeResponse("invalid category")
                    return Response(data)
                serializer = CategorySerializer(category, data=request.data)
                if(serializer.is_valid()):
                    serializer.save()
                    response = getPositiveResponse(
                        "update Category", serializer.data)
                    return Response(response)
                else:
                    data = getNegativeResponse("serializer is not valid")
                    return Response(data) 
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)