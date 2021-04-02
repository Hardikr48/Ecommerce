from djongo import models
from cartitem.models import CartItem
from djongo.models import ArrayField
from account.models import User

ORDER_CHOICES = (('deliverd', 'deliverd'),
                 ('pending', 'pending'),
                 ('reject', 'reject'),
                 ('cancel', 'cancel'),
                 ('shipped', 'shipped'))


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # order_items = ArrayField(models.CharField(max_length=255))
    total_quantity = models.IntegerField()
    total_amount = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile_no = models.IntegerField()
    address = models.TextField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100, choices=ORDER_CHOICES)

    def __str__(self):
        return self.user.email