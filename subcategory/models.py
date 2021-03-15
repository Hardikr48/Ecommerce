from category.models import Category
from django.db import models

class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{} - {}".format(self.name ,self.category)