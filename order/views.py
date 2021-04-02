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
