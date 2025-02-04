from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False, min_length=8)
    address = serializers.CharField(required=False, allow_blank=True)
    phone_no = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'address', 'phone_no', 'user_status')
        extra_kwargs = {
            'password': {'allow_blank': False, 'required':True, 'write_only':True},
        }
        

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'seller', 'name', 'price', 'brand', 'description', 'image', 'category', 'stock', 'created_at', 'updated_at', 'num_ratings', 'avg_rating', 'all_reviews','sale' ,'price_after_sale')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ('id','user', 'status', 'government', 'city', 'street', 'zip_code', 'phone_number', 'status', 'payment_status', 'order_date', 'total_amount', 'total_products')