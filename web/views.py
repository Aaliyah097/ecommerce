from django.shortcuts import render

from catalog.product.repository import ProductFilter, ProductRepository


def index(request):
    return render(request, 'pages/index.html', {})


def catalog_page(request):
    product_filter = ProductFilter(request.GET, queryset=ProductRepository.get_queryset())

    return render(request, 'pages/products.html', {
        'filter': product_filter,
        'products': product_filter.qs
    })
