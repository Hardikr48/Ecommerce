from rest_framework import serializers
from subcategory.models import SubCategory

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("name","category" ,"id")