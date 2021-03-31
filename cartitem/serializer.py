from rest_framework import serializers
from .models import CartItem

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ("id","product","quantity")
    
    def create(self, validated_data):
        try:
            cart = CartItem.objects.get(user=self.context['user'],product=validated_data['product'])
            cart.quantity = validated_data['quantity']

        except CartItem.DoesNotExist:
            cart = CartItem(
                product= validated_data['product'],
                user=self.context['user'],
                quantity=validated_data['quantity']
            )
        cart.save()
        response_data = {
                        'product': cart.product.id,
                        'quantity': cart.quantity,
                        'user':cart.user.id
                    }
        return response_data

class CartListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ("id","product","quantity","user")
