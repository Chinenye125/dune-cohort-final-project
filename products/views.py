from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404 
from .models import Product, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Value
from .forms import ProductForm
from django.contrib import messages
from django.db.models.functions import Lower, Replace

def admin_only(user):
    return user.is_authenticated and user.is_staff


def product_list(request):
    # get search input
    query = request.GET.get('search', '').strip()

    # normalize user input:
    # "Meat Pie" → "meatpie"
    normalized_query = query.lower().replace(' ', '')

    # base queryset
    products = Product.objects.all().order_by('-created_at')

    # annotate products with normalized name (remove spaces + lowercase)
    products = products.annotate(
        normalized_name=Replace(Lower('name'), Value(' '), Value(''))
    )

    # apply search if user typed something
    if normalized_query:
        products = products.filter(
            Q(normalized_name__icontains=normalized_query) |
            Q(category__name__icontains=query)  # category search (normal match)
        )

    context = {
        'products': products,
        'query': query
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)

def category_filter(request, category_name):
    products = Product.objects.filter(category__name__iexact=category_name).order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products, 'category_name': category_name})

def category_list(request):
    categories = Category.objects.all().order_by('-id')
    return render(request, 'products/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category).order_by('-created_at')
    return render(request, 'products/category_detail.html', {'products': products, 'category': category})

@login_required
@user_passes_test(admin_only)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {'form': form})

@login_required
@user_passes_test(admin_only)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {'form': form})

@login_required
@user_passes_test(admin_only)
def product_delete(request, pk):
   product = get_object_or_404(Product, pk=pk)

# Restrict to staff (admins)
   if not request.user.is_staff:
       messages.error(request, "You are not authorized to delete this product.")
       return redirect('product_list')

   if request.method == 'POST':
      product_name = product.name
      product.delete()
      messages.success(request, f'{product_name} deleted successfully.')
      return redirect('product_list')

   return render(request, 'products/product_confirm_delete.html', {'product': product})


class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can create products"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProductDetailAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can update products"},
                status=status.HTTP_403_FORBIDDEN
            )

        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can delete products"},
                status=status.HTTP_403_FORBIDDEN
            )

        product = self.get_object(pk)
        product.delete()

        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )   