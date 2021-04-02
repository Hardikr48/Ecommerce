from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from cartitem.models import CartItem
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    total_amount = serializers.IntegerField(required=False)
    total_quantity = serializers.IntegerField(required=False)

    class Meta:
        model = Order
        exclude = ('user', 'created_date')

    def create(self, validated_data):
        user = self.context.get("user")
        total_quantity = 0
        unit_price = 0
        total_amount = 0
        cart = CartItem.objects.filter(user_id=user.id).values_list('id',flat=True)
        for items_id in cart:
            try:
                cart_item = CartItem.objects.get(id=items_id)
                unit_price = cart_item.product.price
                quantity = cart_item.quantity*unit_price
                total_amount = total_amount+quantity 
                total_quantity = total_quantity+cart_item.quantity
            except:
                error = {
                    'message': f'cart Item Id({cart}) is not persent in your cart'}
                raise serializers.ValidationError(error)
        name = validated_data['name']
        email = validated_data['email']
        mobile_no = validated_data['mobile_no']
        address = validated_data['address']
        city = validated_data['city']
        state = validated_data['state']
        zipcode = validated_data['zipcode']
        order_status = validated_data['order_status']
        order_details = Order(user=user, total_quantity=total_quantity, total_amount=total_amount, name=name, email=email,
                                   mobile_no=mobile_no, address=address, city=city, state=state, zipcode=zipcode, order_status=order_status)
        order_details.save()

        return order_details
