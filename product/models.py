from djongo import models
from django.utils import timezone
from subcategory.models import SubCategory

class Product(models.Model):
    name = models.CharField(unique=True,max_length=255, null=False)
    category = models.CharField(max_length=255, null=False)    
    price = models.FloatField(max_length=17, null=False) 
    sku = models.CharField(max_length=13,help_text="Enter Product Stock Keeping Unit")
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Enter Product Quantity")
    discription = models.CharField(max_length=255, null=False) 
    created_date = models.TimeField(default = timezone.now )
    last_updated = models.TimeField(default = timezone.now,editable=True)
    image = models.ImageField(upload_to= 'app/', blank=True , null=True)
    buffer_stock = models.FloatField(help_text="Enter Product Quantity")

    class Meta:
        db_table = "product"    

    def __str__(self):
        return " {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {}".format(self.name, self.category, self.price,self.sku, self.quantity, self.discription,self.subcategory,self.created_date, self.last_updated,self.image,self.buffer_stock)