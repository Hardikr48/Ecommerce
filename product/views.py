from .models import Product
from .serializer import ProductSerializer, ProductListSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import request
from account.authentication import CustomAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from helper import getNegativeResponse, getPositiveResponse

class ProductViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)
    
    @action(detail=False, methods=["GET"])
    def productlist(self, request):
        try:
            user = self.request.user
            if user:
                product = Product.objects.all()
                serializer = ProductListSerializer(product, many=True)
                data = getPositiveResponse(
                    "product list", serializer.data)
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
                    product = Product.objects.filter(name__startswith=request.data['name'])                
                except Exception:
                    data = getNegativeResponse("product is not valid")
                    return Response(data)
                serializer = ProductListSerializer(product , many= True)
                data = getPositiveResponse("product", serializer.data)
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
                    product = Product.objects.get(id=request.data['id'])
                except Exception:
                    data = getNegativeResponse("product is not valid")
                    return Response(data)
                operation = product.delete()
                data={}
                if operation:
                    data["success"] = "delete successful"
                    response = getPositiveResponse("subcategory", data)
                    return Response(response)
                else:
                    data = getNegativeResponse("delete filed")
                    return Response(data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data) 

    @action(detail=False, methods=["post"])
    def add(self, request):
        print(request.data)
        try:
            user = self.request.user
            if user:
                serializer = ProductSerializer(data=request.data)
                if(serializer.is_valid()):
                    serializer.save()
                    response = getPositiveResponse(
                        "Add subcategory", serializer.data)
                    return Response(response)    
                else:
                    data = getNegativeResponse("serializer is not valid")
                    return Response(data) 
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["PUT"])
    def updateproduct(self,request):
        try:
            user = self.request.user
            print(request.data)
            if user:
                try:
                    product = Product.objects.get(id=request.data['id'])
                except Exception:
                    data = getNegativeResponse("product is not valid")
                    return Response(data) 
                serializer = ProductListSerializer(product, data=request.data)

                if(serializer.is_valid()):
                    serializer.save()
                    response = getPositiveResponse(
                        "update product", serializer.data)
                    return Response(response)
                else:
                    data = getNegativeResponse("serializer is not valid")
                    return Response(data)   
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)
