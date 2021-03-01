from rest_framework.authentication import BaseAuthentication, exceptions
from account.models import BlackList

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' in request.META: 
            token = request.META['HTTP_AUTHORIZATION'][4:]
            try:
                BlackList.objects.get(token=token)
                raise exceptions.AuthenticationFailed('Unauthorized user')
            except BlackList.DoesNotExist:
                pass
