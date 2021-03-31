from djongo import models
from django import forms
from product.models import Product
from account.models import User

class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    

    class Meta:
        db_table = "cartitem"

    def __str__(self):
        return "{} - {} - {}".format(self.product,self.user,self.quantity)


# from django.db import models
# from django.contrib.postgres.fields import ArrayField
# from account.models import User
# from django.conf import settings
# from product.models import Product

# class Cart(models.Model):

#     customer = models.OneToOneField(
#         settings.AUTH_USER_MODEL, related_name='cart', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# class CartItem(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     cart = models.ForeignKey(Cart, related_name='items',
#                             on_delete=models.CASCADE, null=True, blank=True)
#     product = models.ForeignKey(
#         Product, related_name='items', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

#     def __unicode__(self):
#         return '%s: %s' % (self.product.name, self.quantity)
