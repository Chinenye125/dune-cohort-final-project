from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# CATEGORY MODEL
# This stores product categories
# Example:
# Cakes, Drinks, Pastries

class Category(models.Model):

    # Category name
    name = models.CharField(max_length=100)


    # What displays in admin panel
    def __str__(self):
        return self.name




# PRODUCT MODEL
# This stores food products

class Product(models.Model):

    # Product name
    name = models.CharField(max_length=200)


    # Product description/details
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


    # Product price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_by = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,    
        null = True,
        blank = True,
        related_name = 'products'
    )


    # Link product to category
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )


    # Upload product image
    image = models.ImageField(
        upload_to='products/',
        blank=True, 
        null=True
    )

    stock = models.PositiveIntegerField(default=0)


    # Check if product is available
    available = models.BooleanField(default=True)


    # Save date product was created
    created_at = models.DateTimeField(auto_now_add=True)


    # What displays in admin panel
    def __str__(self):
        return self.name