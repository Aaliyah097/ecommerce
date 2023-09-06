from django.shortcuts import render
from django.core.paginator import Paginator

from catalog.product.repository import ProductFilter, ProductRepository


def index(request):
    return render(request, 'copy_pages/index.html', {})


def contacts_page(request):
    return render(request, 'copy_pages/contacts.html', {})


def about_page(request):
    return render(request, 'copy_pages/about.html', {})


def catalog_page(request):
    product_filter = ProductFilter(request.GET, queryset=ProductRepository.get_queryset())

    paginator = Paginator(product_filter.qs, 10)
    page = request.GET.get('page')
    products_per_page = paginator.get_page(page)

    return render(request, 'copy_pages/catalog.html', {
        'filter': product_filter,
        'page': products_per_page,
    })
