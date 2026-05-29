from django.contrib import admin
from.models import Product, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'stock',
        'category',
        'created_at',
    )
    search_fields = ('name', 'category__name')  # allow searching by product name and category name
    list_filter = ('category', 'available')  # add filters for category and availability


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)