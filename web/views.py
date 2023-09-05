from django.shortcuts import render

from catalog.product.repository import ProductFilter, Products


def index(request):
    return render(request, 'pages/index.html', {})


def products_page(request):
    products = Products.objects.all()
    form = ProductFilter(request.GET, queryset=products)

    return render(request, 'pages/products.html', {
        'filter': form,
        'products': form.qs
    })
