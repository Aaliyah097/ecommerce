import datetime

import django_filters
from django import forms
from copy import deepcopy

from django.shortcuts import render
from django.core.paginator import Paginator
from pycbrf import ExchangeRates

from catalog.models import Brands, Currencies, Categories, Products
from catalog.product.repository import ProductFilter, ProductRepository
from catalog.product.brand.repository import BrandRepository
from catalog.category.repository import CategoryRepository
from collections import defaultdict


def index(request):
    categories = CategoryRepository.get_queryset().filter(parent__isnull=True, is_hidden=False)

    brands = BrandRepository.get_queryset().filter(is_hidden=False)

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

    category_slug = request.GET.get('category', None)
    brand_slug = request.GET.get('brand', None)

    category = CategoryRepository.get_by_slug(category_slug)
    chain = CategoryRepository().get_back_chain(category_slug)

    paginator = Paginator(product_filter.qs, 25)

    page = request.GET.get('page')

    products_per_page = paginator.get_page(page)

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']

    if category:
        categories_filter = Categories.objects.filter(parent__slug=category.parent.slug if category.parent else category.slug)
        children = category.get_descendants(include_self=True)

        if brand_slug:
            series_filter = [s[0] for s in Products.objects.filter(brand__slug=brand_slug, category__in=children).order_by('series').distinct('series').values_list('series')]
        else:
            series_filter = []

        if category.parent:
            brands_filter = Brands.objects.filter(
                slug__in=[b[0] for b in
                          Products.objects.filter(category__in=chain).order_by('brand').distinct('brand').values_list(
                              'brand__slug')]
            )
        else:
            brands_filter = Brands.objects.filter(
                slug__in=[b[0] for b in Products.objects.filter(category__in=children).order_by('brand').distinct(
                    'brand').values_list('brand__slug')]
            )
    else:
        categories_filter = Categories.objects.filter(parent__isnull=True)
        brands_filter = Brands.objects.all()
        series_filter = []

    return render(request, 'pages/catalog.html', {
        'filter': product_filter,
        'page': products_per_page,
        'query_params': '&'.join([f"{key}={value}" for key, value in query_params.items()]),
        'breadcrumbs': chain,
        'category': category,
        'usd_rub': float(ExchangeRates(str(datetime.date.today()))['USD'].rate),
        'currency': Currencies.objects.get(name='RUB'),
        'filters': {
            'categories': categories_filter,
            'brands': brands_filter,
            'series': series_filter
        }
    })


def category_page(request, slug):
    category = CategoryRepository.get_by_slug(slug)
    children = category.get_descendants(include_self=True)

    child_categories = sorted(CategoryRepository().get_children(category), key=lambda x: len(x.description), reverse=True)

    for cat in child_categories:
        cat.series = sorted(ProductRepository.get_queryset().filter(category__slug=cat.slug).order_by('series').distinct('series').values_list('series'))

    brand_categories = Brands.objects.filter(
        slug__in=[b[0] for b in ProductRepository.get_queryset().filter(category__in=children, series__isnull=False).order_by('brand').distinct('brand').values_list('brand__slug')]
    )

    for brand in brand_categories:
        brand.series = sorted(ProductRepository.get_queryset().filter(category__in=children, brand=brand, series__isnull=False).order_by('series').distinct('series').values_list('series'))

    return render(request, 'pages/category.html', {
        'category': category,
        'child_categories': child_categories,
        'brand_categories': brand_categories
    })


def product_page(request, brand_slug: str, part_number: str):
    product = Products.objects.get(brand__slug=brand_slug, part_number=part_number)
    # TODO 404 page

    return render(request, 'pages/product.html', {
        'product': product,
        'usd_rub': float(ExchangeRates(str(datetime.date.today()))['USD'].rate),
        'currency': Currencies.objects.get(name='RUB'),
    })
