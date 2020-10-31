from django.shortcuts import render


def home_page(request):
    context = {
        'title': 'Home page',
        'desciption': 'simple home page '
    }

    return render(request, 'homepage.html', context)
