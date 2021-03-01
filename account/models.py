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

