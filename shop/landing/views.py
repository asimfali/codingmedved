from django.http import HttpResponseRedirect
from django.shortcuts import render
from products.models import ProductImage
from .forms import NameForm


def landing(request):
    name = 'simfali'
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
    else:
        form = NameForm

    return render(request, 'landing/landing.html', {'name': name, 'form': form})


def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True)
    return render(request, 'landing/home.html', {'products_images': products_images})
