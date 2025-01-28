from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(_('email address'), unique = True)
    address = models.CharField(max_length = 250, blank = True, null = True)
    phone_no = models.CharField(max_length = 15)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return "{}".format(self.email)


class Seller(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    id_image = models.ImageField(upload_to='id_images', blank=False, null=True) # null=False but temporary =True
    

    def __str__(self):
        return f"{self.user.username} ~ {self.user.email}"

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

def get_unknown_category_id():
    return Category.objects.get_or_create(name="unknown")[0].id

class Products(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=get_unknown_category_id)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def num_ratings(self):
        return self.reviews.count()
    def avg_rating(self):
        ratings = self.reviews.all()
        if ratings.count() == 0:
            return 0
        result = sum(rating.rating for rating in ratings) / len(ratings)
        return round(result, 2)

    def __str__(self):
        return f"{self.name} brand-{self.brand} stock-{self.stock}"


class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=False, blank=False, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=False)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
