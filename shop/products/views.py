from django.shortcuts import render


def stub(request):
    return render(request, 'landing/landing.html')
