from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category


def home(request):
    q = request.GET.get('q')

    if q == None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(
            Q(name__icontains = q) | 
            Q(category__name__icontains = q) |
            Q(tags__name = q)
        ).distinct()

    name = request.user.username
    context = {'name': name, 'products': products}
    return render(request, 'store/home.html', context)

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'store/product-detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'nav.html', context)
