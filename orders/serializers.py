from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    class Meta:
        model = OrderItem
        fields = ('id','order','product','product_detail','quantity','price')
        read_only_fields = ('price','product_detail')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id','user','status','total_amount','payment_reference','items','created_at')
        read_only_fields = ('user','total_amount','created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        total = 0
        for item in items_data:
            product = item['product']
            qty = item.get('quantity',1)
            price = product.price
            OrderItem.objects.create(order=order, product=product, quantity=qty, price=price)
            total += price * qty
        order.total_amount = total
        order.save()
        return order
