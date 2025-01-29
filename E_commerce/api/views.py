from django.shortcuts import render
from .models import *
from .serializers import ProductsSerializer, CategorySerializer, ReviewsSerializer, OrderSerializer, OrderItemSerializer, CustomUserSerializer, RegisterSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from .filtters import *
from datetime import  timedelta   #datetime,
from django.utils import timezone
#from rest_framework.pagination import LimitOffsetPagination
#from rest_framework.authtoken.models import Token



# Create your views here.

# products
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products(request):
    if request.method == 'GET':
        products = ProductsFilter(request.GET, queryset=Products.objects.all().order_by('id'))
        # new products is filtered --> add .qs to it
        serializer = ProductsSerializer(products.qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product(request, pk):
    try:
        product = Products.objects.get(id=pk)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductsSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# categories
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categories(request):    
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except :
        return Response({"error", "category not found"})
    if request.method == 'GET':
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Reviews
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reviews(request):
    if request.method == 'GET':
        reviews = Reviews.objects.all()
        serializer = ReviewsSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review(request, pk):
    try:
        review = Reviews.objects.get(id=pk)
    except Reviews.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReviewsSerializer(review, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ReviewsSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def order(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"error":"order not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orderitems(request):
    if request.method == 'POST':
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        orderitems = OrderItem.objects.all()
        serializer = OrderItemSerializer(orderitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def orderitem(request, pk=None):
    try:
        orderitem = OrderItem.objects.get(id=pk)
    except OrderItem.DoesNotExist:
        return Response({"error":"order item not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = OrderItemSerializer(orderitem, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = OrderItemSerializer(orderitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        orderitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            if CustomUser.objects.filter(email=request.data['email']).exists():
                return Response({"error": "email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            if CustomUser.objects.filter(username=request.data['username']).exists():
                return Response({"error": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            response = {
                "message": "user was created successfully",
                "user": serializer.data # temporary
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(email=request.data['email'])
        except CustomUser.DoesNotExist:
            return Response({"error":"Your E-mail doesn't exist"})
        token = get_random_string(40)
        user.reset_password_token = token
        user.reset_password_expires = timezone.now() + timedelta(minutes=5)
        user.save()

        link = f"http://127.0.0.1:8000/api/reset-password/{token}/"
        body = f"Your link for reset your password : {link}"
        send_mail(
            'Reset Password',
            body,
            'from ecommerce',
            [request.data["email"]],
        )
        return Response({"message": "Email was sent successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, token=None):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(reset_password_token=token)
        except CustomUser.DoesNotExist:
            return Response({"error": "Your token doesn't exist"})
        if user.reset_password_expires < timezone.now():
            return Response({"error": "Your token has expired"})
        if request.data['password'] != request.data['confirmPassword']:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.password = make_password(request.data['password'])
            user.reset_password_token = None
            user.reset_password_expires = None
            user.save()
            return Response({"message": "Password was reset successfully"}, status=status.HTTP_200_OK)
        


'''
---> admin and staff sections
'''

#products section
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):
    if request.method == 'POST':
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def update_product(request, pk=None):
    try:
        product = Products.objects.get(id=pk)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        message = {
            'message': 'Product deleted successfully'
        }
        return Response(message, status=status.HTTP_204_NO_CONTENT)


# category section
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def update_category(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response({"error":"category not found"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        category.delete()
        return Response({"message": "category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
