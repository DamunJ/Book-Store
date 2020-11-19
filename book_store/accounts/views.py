from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .form import LoginForm, RegisterForm, ProfileUpdate
from .models import Profile


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


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


User = get_user_model()


def register(request):
    form = RegisterForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('/')
    context = {'form': form}
    if form.is_valid():
        username, email, password = request.POST.get('username'), request.POST.get('email'), request.POST.get(
            'password')

        new_user = User.objects.create_user(username=username, password=password, email=email)
        Profile(user=new_user).save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return redirect('/')
    return render(request, 'accounts/register.html', context)

@login_required
def profile(request):
    context = {
        'name': 'salam'
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_update(request):
    form = ProfileUpdate(request.POST or None, instance=request.user.profile)
    context = {
        'form': form,
        'header': 'ProfileUpdate',
    }
    if request.method == "POST":
        if form.is_valid():
            form = ProfileUpdate(request.POST, instance= request.user.profile)
            form.save()
    return render(request, 'accounts/profile_edit.html', context)
