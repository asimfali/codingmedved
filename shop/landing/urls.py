from landing import views
from django.urls.conf import path

urlpatterns = [
    path('', views.landing, name='landing')
]
