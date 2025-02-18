from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import *
from .serializers import ProductsSerializer, CategorySerializer, ReviewsSerializer, OrderSerializer, OrderItemSerializer, CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from .filtters import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import  timedelta   #datetime,
from django.utils import timezone
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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
review_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID التقييم'),
        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='صانع التقييم'),
        'product': openapi.Schema(type=openapi.TYPE_OBJECT, description='المنتج المقييم'),
        'rating': openapi.Schema(type=openapi.TYPE_NUMBER, description='درجة التقييم'),
        'review': openapi.Schema(type=openapi.TYPE_STRING, description='التعليق'),
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, description='التاريخ'),
    },
)

@swagger_auto_schema(
    method='post',
    request_body=ReviewsSerializer,  # استخدام الـ Serializer كـ Request Schema
    responses={
        200: review_schema,  # استخدام الـ Schema المخصص كـ Response
        400: 'Bad Request',
    },
    operation_description="إنشاء منتج جديد",
)
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

order_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID الطلب'),
        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='المستخدم اللذي قام بالطلب'),
        'government': openapi.Schema(type=openapi.TYPE_STRING, description='المحافظة'),
        'city': openapi.Schema(type=openapi.TYPE_STRING, description='المدينة'),
        'street': openapi.Schema(type=openapi.TYPE_STRING, description='الشارع'),
        'zip_code': openapi.Schema(type=openapi.TYPE_STRING, description='الرمز البريدي'),
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='رقم الهاتف'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='الحالة'),
        'payment_status': openapi.Schema(type=openapi.TYPE_STRING, description='حالة الدفع'), 
        'order_date': openapi.Schema(type=openapi.TYPE_STRING, description='التاريخ'), 
    },
)

@swagger_auto_schema(
    method='post',
    request_body=OrderSerializer,  # استخدام الـ Serializer كـ Request Schema
    responses={
        200: order_schema,  # استخدام الـ Schema المخصص كـ Response
        400: 'Bad Request',
    },
    operation_description="إنشاء منتج جديد",
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
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
        return Response({'message': 'Order has been deleted'}, status=status.HTTP_204_NO_CONTENT)

    
orderitem_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID'),
        'order': openapi.Schema(type=openapi.TYPE_OBJECT, description='اسم الطلب'),
        'product': openapi.Schema(type=openapi.TYPE_OBJECT, description='المنتج المطلوب'),
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='الكمية'),
    },
)

@swagger_auto_schema(
    method='post',
    request_body=OrderItemSerializer,  # استخدام الـ Serializer كـ Request Schema
    responses={
        200: orderitem_schema,  # استخدام الـ Schema المخصص كـ Response
        400: 'Bad Request',
    },
    operation_description="إنشاء منتج جديد",
)

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
        return Response({'message': 'Order has been deleted'}, status=status.HTTP_204_NO_CONTENT)
    

user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID المستخدم'),
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='اسم المستخدم'),
        'email': openapi.Schema(type=openapi.TYPE_OBJECT, description='البريد الالكتروني'),
        'first_name': openapi.Schema(type=openapi.TYPE_NUMBER, description='الاسم الاول'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='الاسم الاخير'),
        'address': openapi.Schema(type=openapi.TYPE_OBJECT, description='العنوان'),
        'phone_no': openapi.Schema(type=openapi.TYPE_STRING, description='رقم الهاتف'),
        'user_status': openapi.Schema(type=openapi.TYPE_STRING, description='حالة المستخدم'),
    },
)

@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,  # استخدام الـ Serializer كـ Request Schema
    responses={
        200: user_schema,  # استخدام الـ Schema المخصص كـ Response
        400: 'Bad Request',
    },
    operation_description="إنشاء مستخدم جديد",
)
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



user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_OBJECT, description='البريد الالكتروني'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='كلمة المرور'),},
)

@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,  # استخدام الـ Serializer كـ Request Schema
    responses={
        200: user_schema,  # استخدام الـ Schema المخصص كـ Response
        400: 'Bad Request',
    },
    operation_description="تسجيل دخول للمستخدم",
)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=request.data['email'], password=request.data['password'])
            if user is not None:
                refresh = RefreshToken.for_user(user)
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'user': user_serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK
                    )
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
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
product_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID العنصر'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='اسم العنصر'),
        'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='سعر العنصر'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='وصف العنصر'),
        'seller': openapi.Schema(type=openapi.TYPE_OBJECT, description='البائع (staff_user)'),
        'brand': openapi.Schema(type=openapi.TYPE_STRING, description='الماركة'),
        'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='الصنف'),
        'image': openapi.Schema(type=openapi.TYPE_FILE, description='صورة العنصر'),
        'stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='عدد المنتجات'), 
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, description='تاريخ الإضافة'), 
        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description='تاريخ التعديل'),
        'num_ratings': openapi.Schema(type=openapi.TYPE_INTEGER, description='عدد التقييمات'), 
        'avg_rating': openapi.Schema(type=openapi.TYPE_NUMBER, description='متوسط التقييمات'), 
        'all_reviews': openapi.Schema(type=openapi.TYPE_OBJECT, description='التقييمات و التعليقات'),
    },
)

@swagger_auto_schema(
    method='post',
    request_body=ProductsSerializer,  # استخدام الـ Serializer كـ Request Schema
    responses={
        200: product_schema,  # استخدام الـ Schema المخصص كـ Response
        400: 'Bad Request',
    },
    operation_description="إنشاء منتج جديد",
)
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
category_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID الفئة'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='اسم الفئة'),
    },
)

@swagger_auto_schema(
    method='post',
    request_body=CategorySerializer,  # استخدام الـ Serializer كـ Request Schema
    responses={
        200: category_schema,  # استخدام الـ Schema المخصص كـ Response
        400: 'Bad Request',
    },
    operation_description="إنشاء منتج جديد",
)
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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user(request, pk=None):
    try:
        user = CustomUser.objects.get(id=pk)
    except CustomUser.DoesNotExist:
        return Response({"error":"user not found"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = CustomUserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"error":"order not found"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        order.status = request.data['status']
        order.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

