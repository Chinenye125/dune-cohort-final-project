from django.urls import path 
from . import views  #'.' means import from the current app package

urlpatterns = [
    path('', views.product_list, name='product_list'),  # this is the url for the product list page
    path('<int:pk>/', views.product_detail, name='product_detail'),  #
    # this is the url for the product detail page, it takes an integer parameter 'pk' which is the primary key of the product
]