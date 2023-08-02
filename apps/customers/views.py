import sweetify

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomerForm
from .models import Customer


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            sweetify.success(request, 'User registered succsefully!',
                             text=f'Welcome {user.username}', timer=2000)
            return redirect('home')
        else:
            sweetify.error(
                request, 'An error ocurred during the registration', timer=2000)

    context = {'form': form}
    return render(request, 'customers/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            sweetify.success(request, f'Welcome {user.username}', timer=1500)
            return redirect('home')
        else:
            sweetify.error(
                request, 'Username or password invalid, try again', timer=1500)
            return redirect('login')

    return render(request, 'customers/login.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def profile_page(request):
    user = Customer.objects.get(user=request.user)
    context = {'user': user}

    return render(request, 'customers/profile-page.html', context)


@login_required(login_url='login')
def edit_customer_info(request):
    user = Customer.objects.get(user=request.user)
    form = CustomerForm(initial={
        'address': user.address,
        'phone_number': user.phone_number,
        'document_id': user.document_id
    })

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Info updated successfully!')
            return redirect('profile-page')

    context = {'form': form}
    return render(request, 'customers/profile-update.html', context)
