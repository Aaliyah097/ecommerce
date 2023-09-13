from django.shortcuts import render
from django.core.paginator import Paginator

from catalog.product.repository import ProductFilter, ProductRepository
from catalog.product.brand.repository import BrandRepository
from catalog.category.repository import CategoryRepository


def index(request):
    categories = []

    for cat in CategoryRepository.get_queryset():
        categories.append({
            'category': cat,
            'amount': ProductRepository.get_queryset().filter(category=cat).count()
        })

    brands = []

    for brand in BrandRepository.get_queryset():
        brands.append({
            'brand': brand,
            'amount': ProductRepository.get_queryset().filter(brand=brand).count()
        })

    return render(request, 'pages/index.html', {
        'brands': brands,
        'categories': categories
    })


def contacts_page(request):
    return render(request, 'pages/contacts.html', {})


def about_page(request):
    return render(request, 'pages/about.html', {})


def catalog_page(request):
    product_filter = ProductFilter(request.GET, queryset=ProductRepository.get_queryset())

    paginator = Paginator(product_filter.qs, 10)
    page = request.GET.get('page')
    products_per_page = paginator.get_page(page)

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']

    return render(request, 'pages/catalog.html', {
        'filter': product_filter,
        'page': products_per_page,
        'query_params': '&'.join([f"{key}={value}" for key, value in query_params.items()]),
    })
