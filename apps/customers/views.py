from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import sweetify

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'User registered succsefully!')
            return redirect('home')
        else:
            messages.error(request, 'An error ocurred during the registration')

    context = {'form':form}
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
            sweetify.success(request, 'Welcome ' + user.username , timer=2000)
            return redirect('home')
        else:
            messages.error(request, 'Username or password invalid, try again')
            return redirect('login')
        
    return render(request, 'customers/login.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')