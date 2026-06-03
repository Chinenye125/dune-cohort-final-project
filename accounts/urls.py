from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import CustomLoginView, logout_view,  register_view


urlpatterns = [  # Use our custom login view
  path('login/', CustomLoginView.as_view(), name='login'),
  path('register/', register_view, name='register'),
  path('logout/', logout_view, name='logout'),
]