# E-commerce API (Django REST Framework)

مشروع API لمتجر إلكتروني مبني باستخدام Django REST Framework مع نظام مصادقة متكامل (JWT) وإدارة كاملة للمنتجات، الطلبات، التقييمات، والمستخدمين.

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

## المميزات الرئيسية
- مصادقة باستخدام JWT Token
- إدارة كاملة للمستخدمين (تسجيل، دخول، إعادة تعيين كلمة المرور)
- CRUD operations للمنتجات والفئات
- نظام طلبات مع تفاصيل العناصر
- تقييمات للمنتجات
- صلاحيات مستندة على الأدوار (عادي vs أدمن)

## التقنيات المستخدمة
- Python 3.9+
- Django 4.2
- Django REST Framework
- Simple JWT (للـ Authentication)
- PostgreSQL (أو أي قاعدة بيانات أخرى)

## التثبيت

### المتطلبات المسبقة
- Python 3.9+
- Pipenv (أو virtualenv)
- PostgreSQL

### الخطوات
1. استنساخ المشروع:
   ```bash
   git clone https://github.com/DevMo7md/E-commerce-API_DjangoRest.git
   cd E-commerce-API_DjangoRest
   pip install requirments.txt