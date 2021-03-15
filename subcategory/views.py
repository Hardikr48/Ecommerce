from .models import SubCategory
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from account.authentication import CustomAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from subcategory.serializer import SubCategorySerializer
from helper import getNegativeResponse, getPositiveResponse

    @action(detail=False, methods=["post"])
    def add(self, request):
        try:
            user = self.request.user
            if user:
                serializer = SubCategorySerializer(data=request.data)
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
