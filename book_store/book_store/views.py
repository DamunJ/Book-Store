from django.shortcuts import render


def home_page(request):
    context = {
        'title': 'Home page',
        'text': 'simple home page '
    }

    return render(request, 'Home_page.html', context)
