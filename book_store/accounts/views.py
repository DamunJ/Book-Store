from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .form import LoginForm, RegisterForm
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
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        new_user = User.objects.create_user(username=username, password=password, email=email)
        print(new_user)
        return redirect('/')
    return render(request, 'accounts/register.html', context)
