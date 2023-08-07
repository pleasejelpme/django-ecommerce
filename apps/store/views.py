import json
import sweetify

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Order, ProductOrder
from .forms import ProductCreateForm, CheckoutForm


def home(request):
    q = request.GET.get('q')
    if q is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(category__name__icontains=q) |
            Q(tags__name=q)
        ).distinct()

    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }

    # FUNCTIONALITY TO BE IMPLEMENTED: The "add to cart" button should not be
    # shown if the customer already have the product in their shopping cart

    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     products_in_order = Order.get_active_order_by_customer(
    #         customer).productorder_set.all()
    #     context['products_in_order'] = products_in_order

    return render(request, 'home.html', context)


def category_list(request):
    context = {
        'categories': Category.objects.all(),
        'total_products': Product.objects.count(),
    }
    return render(request, 'offcanvas.html', context)


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
            sweetify.success(request, 'Product added successfully')
            return redirect('home')
        else:
            sweetify.error(request, 'An error ocurred')

    context = {'form': form}
    return render(request, 'store/product-create.html', context)


@login_required(login_url='login')
def shopping_cart(request):
    if request.method == 'POST':
        customer = request.user.customer
        data = json.loads(request.body)
        try:
            product_id, action = data.get('product_id'), data.get('action')
        except:
            print('error')

        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(
            customer=customer, completed=False)
        product_order, created = ProductOrder.objects.get_or_create(
            order=order, product=product)

        #  It checks if it is the first time that the product is added to
        #  the shopping cart and sends a messsage
        if created:
            sweetify.success(request, 'Product added to the cart', timer=2000)


#  Checks the button that was clicked (add, remove or clear)

        #  If the action is add checks if there is enough stock of the
        #  product, otherwise sends a message of not enough stock
        if action == 'add':
            if product_order.quantity == product.stock:
                sweetify.warning(
                    request, 'Maximum products available!', timer=2000)
            else:
                product_order.quantity = product_order.quantity + 1
                product_order.save()

        #  If the action is remove it removes 1 product from the total
        #  in the shopping cart
        if action == 'remove':
            product_order.quantity = product_order.quantity - 1
            product_order.save()

        #  If the action is clear it removes all individual products
        #  from the shopping cart
        if action == 'clear':
            print('clear')
            product_order.delete()

        #  It checks if the quantity of the product is zero, and if it
        #  is zero then the product is removed from the shopping cart
        if product_order.quantity <= 0:
            product_order.delete()

        return JsonResponse(data, safe=False)

    if request.method == 'GET':
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, completed=False)
        products = list(order.productorder_set.all())

        context = {
            'order': order,
            'products': products
        }
        return render(request, 'store/shopping-cart.html', context)


@login_required(login_url='login')
def checkout(request, pk):
    customer = request.user.customer
    order = Order.objects.get(id=pk)
    if order.get_total_products == 0:
        return redirect('home')

    form = CheckoutForm(initial={
        'address': customer.address
    })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.customer = customer
            checkout.order = order
            checkout.save()
            sweetify.success(request, 'Payment completed!')
            return redirect('home')

    context = {'form': form, 'order': order}
    return render(request, 'store/checkout.html', context)
