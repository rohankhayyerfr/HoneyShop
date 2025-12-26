from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('accounts:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('accounts:register')

        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return redirect('accounts:register')

        # create user (درست)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        print("REDIRECTING TO HOME")
        # ذخیره full_name
        user.first_name = full_name
        user.save()

        login(request, user)


        return redirect('accounts:login')

    return render(request, "accounts/register.html")


def user_logout(request):
    logout(request)
    return redirect('store:home')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('store:home')

        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')