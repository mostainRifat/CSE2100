from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from cart.models import Cart, CartItem
def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store')
    return render(request, 'accounts/register.html', {'form':form})

def profile(request):
    return render(request, 'accounts/dashboard.html')

def user_login(request):
    if request.method == 'POST':
        
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = user_name, password = password)
        # print(user)
        # ekhono login hoy nai
        if user is not None:  
            login(request, user)
            # login hoye geche
            ##here is the problem
            session_key = get_create_session(request)

            try:
                cart = Cart.objects.get(cart_id=session_key)
            except Cart.DoesNotExist:
                cart = None

            if cart:
                cart_items = CartItem.objects.filter(cart=cart)
                for item in cart_items:
                    item.user = user
                    item.save()
            return redirect('store')
        else:
            # Incorrect credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
            
    return render(request, 'accounts/signin.html')

def user_logout(request):
    logout(request)
    return redirect('login')