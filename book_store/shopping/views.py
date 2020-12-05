from django.shortcuts import render


# Create your views here.
def main(request):
    context = {}
    return render(request, 'shopping/start_rating_test.html', context)
