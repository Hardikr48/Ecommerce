from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from account.authentication import CustomAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from order.models import Order
from helper import getNegativeResponse
from account.helper import getPositiveResponse
from rest_framework.exceptions import ValidationError
from order.serializer import OrderSerializer

class OrderItemViewSet(viewsets.ViewSet):

    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    
    @action(detail=False, methods=["GET"])
    def listorder(self, request=None):
        try:
            user = self.request.user    
            if user:
                user = request.user
                order_items = Order.objects.filter(user=user) 
                serializer = OrderSerializer(order_items, many=True)
                response = getPositiveResponse("User list", serializer.data)
                return Response(response)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["post"])
    def createorder(self, request):
        try:
            user = self.request.user
            if user:
                serializer = OrderSerializer(data=request.data, context={
                    'user': request.user})
                if serializer.is_valid():
                    serializer.save()
                    response = getPositiveResponse(
                        "add order ", serializer.data)
                    return Response(response)
                else:
                    data = getNegativeResponse("serializer is not valid")
                    return Response(data) 
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["POST"])
    def rejectorder(self, request):
        try:
            user = self.request.user
            if user:
                order_status = request.data['status']
                user = request.user
                if not order_status == "cancel":
                    if not user.is_superuser:
                        raise ValidationError(
                            {'errror': 'Only Super User perform this action'})
                try:
                    order = Order.objects.get(pk=request.data['id'])
                except Exception:
                    data = getNegativeResponse("order is not valid")
                    return Response(data)
                
                order.order_status=request.data['status']
                order.save()
                response = getPositiveResponse(
                    "Reject Order", order.order_status)
                return Response(response)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)

    @action(detail=False, methods=["post"])
    def search(self, request):
        try:
            user = self.request.user
            if user:
                try:
                    order = Order.objects.filter(id=request.data['id']) 
                except Exception:
                    data = getNegativeResponse("order is not valid")
                    return Response(data)
                serializer = OrderSerializer(order , many= True)
                data = getPositiveResponse("order", serializer.data)
                return Response(data)
        except Exception:
            data = getNegativeResponse("unauthorized user")
            return Response(data)