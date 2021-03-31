from django.shortcuts import render

from rest_framework import  viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.messages import constants
from django.db.models import Q
from account.authentication import CustomAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny ,IsAuthenticated
from .serializer import CartSerializer
from .models import CartItem
from account.models import User
from cartitem.serializer import CartListSerializer
import product
from product.models import Product
from product.serializer import ProductListSerializer
from helper import getNegativeResponse, getPositiveResponse


class CartViewSet(viewsets.ViewSet):

    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=["GET"])
    def cartlist(self, request):
        try:
            user = self.request.user
            if user:
                queryset = CartItem.objects.all()
                serializer = CartListSerializer(queryset, many=True)
                data = getPositiveResponse(
                    "List Of Cart", serializer.data)
                return Response(data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["GET"])
    def clearcart(self, request):
        try:
            user = self.request.user
            if user:
                cart = CartItem.objects.all()
                operation = cart.delete()
                data={}
                if operation:
                    data["success"] = "Cart empty"
                else:
                    data["failure"] = "Cart is not empty"
                return Response(data=data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["post"])
    def delete(self, request):
        try:
            print(request.data)
            user = self.request.user
            if user:
                try:
                    cart = CartItem.objects.get(product_id=request.data['product'])
                except:
                    pass
                try:
                    cart = CartItem.objects.get(user_id=request.data['user'])
                except:
                    pass

                operation = cart.delete()
                data={}
                if operation:
                    data["success"] = "delete successful"
                else:
                    data["failure"] = "delete filed"
                return Response(data=data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["post"])
    def addcart(self, request):
        try:   
            user = self.request.user
            if user:
                context={
                    "user":user
                }
                print(context)
                serializer =  CartSerializer(data=request.data ,context=context)
                if(serializer.is_valid()):
                    response_data=serializer.save()
                    response = getPositiveResponse(
                        "Add cart", response_data)
                    return Response(response)    
                else:
                    data = getNegativeResponse("product is not valid")
                    return Response(data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)
