from django.shortcuts import render


def home_page(request):
    context = {
        'title': 'Home page',
        'description': 'simple home page '
    }

    return render(request, 'homepage.html', context)