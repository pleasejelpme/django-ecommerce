from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from .models import Product, Category, Order, ProductOrder
from apps.customers.models import Customer
from django.contrib.auth.decorators import login_required
from .forms import ProductCreateForm, CheckoutForm
import json
import sweetify


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


def category_list(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'aside.html', context)

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

@login_required(login_url='login')
def update_shopping_cart(request):
    if request.method == 'POST':
        customer = request.user.customer
        data = json.loads(request.body)
        product_id = data['product_id']
        action = data['action']
        product = Product.objects.get(id=product_id)

        order, created = Order.objects.get_or_create(customer=customer)
        product_order, created = ProductOrder.objects.get_or_create(order=order, product=product)
        if created:
            sweetify.success(request, 'Product added to the cart', timer=2000)

        if action == 'add':
            try:
                product_order.quantity < product.stock
            except:
                raise ValueError('Not enough stock')
            product_order.quantity = product_order.quantity + 1


        elif action == 'remove':
            product_order.quantity = product_order.quantity - 1           

        product_order.save()

        if product_order.quantity <= 0:
            product_order.delete()

        print('Product: ', product_id, 'Action: ', action)

    return JsonResponse('Product added', safe=False)

@login_required(login_url='login')
def shipping_address(request, pk):
    customer = request.user.customer
    order = Order.objects.get(id=pk)
    form = CheckoutForm()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.customer = customer
            checkout.order = order
            checkout.save()
            sweetify.success(request, 'Payment completed!')

    context = {'form': form, 'order': order}
    return render(request, 'store/checkout.html', context)

    

