from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm, CategoryForm

def home_view(request):
    q = request.GET.get('q')
    if q == None:
        product = Product.objects.all()
    else:
        product = Product.objects.filter(
            Q(name__icontains = q) | 
            Q(category__name__icontains = q)
            )
    
    category = Category.objects.all()
    context = {
        'product':product,  
        'category':category
        }

    return render(request, 'home.html', context)

@login_required(login_url='login')
def create_product_view(request):
    if request.user.is_staff:
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        context = {'form':form}
        return render(request, 'products/product_create.html', context)
    else:
        return redirect('home')

@login_required(login_url='login')
def create_category_view(request):
    if request.user.is_staff:
        form = CategoryForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST)            
            if form.is_valid():    
                form.save()
                return redirect('home')
        context = {'form':form}
        return render(request, 'products/category_create.html', context)
    else:
        return redirect('home')

@login_required(login_url='login')
def delete_view(request, id):
    if request.user.is_staff:
        product = Product.objects.get(id=id)
        if request.method == 'POST':
            product.delete()
            return redirect('home')
        return render(request, 'delete.html', {'obj':product})

@login_required(login_url='login')
def update_product_view(request, id):
    if request.user.is_staff:
        product = Product.objects.get(id=id)
        form = ProductForm(instance=product)
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('home')
        context = {'form':form}
        return render(request, 'products/update_product.html', context)
    else:
        return redirect('home')

def product_detail_view(request, id):
    product = Product.objects.get(id=id)
    context = {'product':product}
    return render(request, 'products/product_detail.html', context)

def product_list_view(request):
    product_list = Product.objects.all()
    context = {'product':product_list}
    return render(request, 'products/product_list.html', context)
