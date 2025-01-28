import django_filters
from .models import Products

class ProductsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    category_keyword = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains")  
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte") 
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte") 

    class Meta:
        model = Products
        fields = ('category', 'brand', 'keyword', 'min_price', 'max_price')
