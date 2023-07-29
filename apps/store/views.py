from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from .models import Product, Category, Order
from apps.customers.models import Customer
from django.contrib.auth.decorators import login_required
from .forms import ProductCreateForm


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

    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'home.html', context)


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'store/product-detail.html', context)

@login_required(login_url='login')
def product_create(request):
    form = ProductCreateForm()
    if request.method == 'POST':
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully')
            return redirect('home')
        else:
            messages.error(request, 'An error ocurred')
    
    context = {'form':form}
    return render(request, 'store/product-create.html', context)

@login_required(login_url='login')
def shopping_cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer = customer)
    products = order.productorder_set.all()

    context = {'products': products, 'order': order}
    return render(request, 'store/shopping-cart.html', context)

def update_shopping_cart(request):
    return JsonResponse('Product added: ', safe=False)


    

