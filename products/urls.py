from django.urls import path 
from. import views  #'.' means import from the current app package

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),

    path('add/', views.product_create, name='product_create'),
    path('edit/<int:pk>/', views.product_update, name='edit_product'),
    path('delete/<int:pk>/', views.product_delete, name='delete_product'),

    path('category/<str:category_name>/', views.category_filter, name='category_filter'),

    path('api/products/', views.ProductListAPIView.as_view(), name='api_products'),

    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),

    path('<int:pk>/', views.product_detail, name='product_detail'),
]   