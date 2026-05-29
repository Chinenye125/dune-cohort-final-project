from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404 
from .models import Product, Category

from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Value
from django.db.models.functions import Lower, Replace
from .models import Product


def product_list(request):
    # get search input
    query = request.GET.get('search', '').strip()

    # normalize user input:
    # "Meat Pie" → "meatpie"
    normalized_query = query.lower().replace(' ', '')

    # base queryset
    products = Product.objects.all()

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