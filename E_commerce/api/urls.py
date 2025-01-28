from django.urls import path, include
from . import views
urlpatterns = [
    # products
    path('products/', views.products),
    path('products/<int:pk>/', views.product),
    path('create-product/', views.create_product),
    path('update-product/<int:pk>/', views.update_product),
    # categories
    path('categories/', views.categories),
    path('categories/<int:pk>/', views.category),
    path('create-category/', views.create_category),
    path('update-category/<int:pk>/', views.update_category),
    # reviews
    path('reviews/', views.reviews),
    path('reviews/<int:pk>/', views.review),
    # Orders
    path('orders/', views.orders),
    path('orders/<int:pk>/', views.order),
    path('orderitems/', views.orderitems),
    path('orderitems/<int:pk>/', views.orderitem),
    #login and authorization
    path('register/', views.register),
]
