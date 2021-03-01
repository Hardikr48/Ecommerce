import string
from django.contrib.messages import constants
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
import random
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone
from account.models import BlackList
from rest_framework.response import Response
from ecommerce import settings




def getPositiveResponse(msg, data={}):
    response = {}
    response['status'] = constants.SUCCESS
    response['message'] = msg
    response['result'] = data
    return response
def getNegativeResponse(msg, status_code=400, result={}):
    response = {}
    response['status'] = constants.FAIL
    response['message'] = msg
    response['result'] = result
    response['statusCode'] = status_code
    return response

def expires_in(token):
    time_elapsed = settings.TOKEN_EXPIRED_AFTER_SECONDS1 
    left_time  = settings.TOKEN_EXPIRED_AFTER_SECONDS - time_elapsed
    if time_elapsed >= left_time: 
        black_list_token = BlackList(token=token.verification_token)
        black_list_token.save()
        return Response(black_list_token)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user):
        return (
            six.text_type(user.pk) +six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()

def randomGeneratorCode(size=25, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
