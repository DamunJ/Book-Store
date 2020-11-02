from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .form import  LoginForm
from django.urls import reverse

def login_page(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    context = {
        "form": form,
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = next_url if next_url else reverse('homepage')
            return HttpResponseRedirect(redirect_url)
        else:
            context = {
                "form": form,
                "error": "کاربری با این مشخصات یافت نشد!",
            }
    return render(request, 'accounts/login.html', context)

def logout():
    pass