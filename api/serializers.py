from rest_framework.serializers import ModelSerializer
from main import models

class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

class CartSerializer(ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'

class CartItemSerializer(ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = '__all__'