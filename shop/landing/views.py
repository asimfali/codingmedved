from django.shortcuts import render


def landing(request):
    name = 'simfali'
    return render(request, 'landing/landing.html', {'name': name})
