from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(Products)
admin.site.register(Seller)
admin.site.register(Category)
class CustomUserAdmin(UserAdmin):
    # عرض الأعمدة في قائمة المستخدمين
    list_display = ('id', 'username', 'email', 'phone_no', 'address', 'is_staff', 'is_superuser')
    
    # الحقول التي يجب أن تكون قابلة للقراءة فقط في صفحة التفاصيل
    readonly_fields = ('id', 'last_login', 'date_joined')

    # تخصيص الحقول التي يمكن عرضها عند إضافة مستخدم جديد
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal Info', {
            'fields': ('address', 'phone_no'),
        }),
    )

    # تخصيص الحقول التي يمكن عرضها عند تعديل مستخدم
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'address', 'phone_no')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # إضافة إمكانية البحث حسب email و username
    search_fields = ('email', 'username')

# تسجيل النموذج المخصص في لوحة الإدارة
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Reviews)