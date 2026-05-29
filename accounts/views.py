from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

# Create your views here.

def register_view(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      # save() creates the User record in the database
      user = form.save()
      # Log the new user in immediately after registration
      login(request, user)
      return redirect('home')
  else:
    form = RegistrationForm()
  return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
  # request.user is the logged-in User object
  # request.user.is_authenticated is True when the user is logged in
  if request.user.is_authenticated:
    username = request.user.username
    email = request.user.email
    is_staff = request.user.is_staff
  return render(request, 'accounts/dashboard.html', {'user': request.user})

class CustomLoginView(LoginView):
  template_name = 'accounts/login.html' 



