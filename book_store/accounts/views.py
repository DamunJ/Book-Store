from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .form import  LoginForm

def login_page(request):
    form = LoginForm(request.POST or None)
    print(request.user.is_authenticated)
    context = {
        'title': 'Login',
        "header": 'login',
        "form": form,
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context["form"] = LoginForm
        else:
            pass

    return render(request, 'accounts/login.html', context)
