from djongo import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    mobile_number = models.CharField(max_length=12, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(
        unique=True, max_length=255, null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    address = models.TextField(max_length=2500,blank=False, null=False) 
    city = models.CharField(max_length=100,blank=True)
    state =  models.CharField(max_length=100,blank=True)
    zipcode= models.IntegerField(blank=True)
    objects = UserManager()

    class Meta:
        db_table = "user"

    def __str__(self):
        return "{} - {} - {}- {} - {} - {} -{} - {} - {} - {} ".format(self.first_name, self.last_name, self.mobile_number,self.email,self.username ,self.address,self.city,self.state,self.zipcode ,self.created_datetime)

class BlackList(models.Model):
    token = models.TextField()

class UserAccessToken(models.Model):
    token = models.TextField()
    user = models.ForeignKey(
        'User',
        on_delete=models.DO_NOTHING
        )

    def __str__(self):
        return "{} - {}".format(self.token, self.user )

class UserVerification(models.Model):
    USER_VERIFICATION_TYPES = (
        ('VERIFY', 'email_verification'),
        ('FORGOT', 'forgot_password')
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.DO_NOTHING
        )
    verification_token = models.CharField(max_length=6, default="")
    verification_type = models.CharField(
        max_length=15, choices=USER_VERIFICATION_TYPES, default=USER_VERIFICATION_TYPES[0][0])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -{} -{} -{} -{}".format(self.USER_VERIFICATION_TYPES, self.verification_token, self.user,self.verification_type ,self.created)    
