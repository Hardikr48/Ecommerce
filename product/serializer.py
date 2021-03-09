from .models import Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model = Product
        fields = ("id","name","category","price","sku","quantity","discription","image","buffer_stock","subcategory")
    
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id","name","category","price","sku","quantity","discription","image","created_date","last_updated","buffer_stock","subcategory")