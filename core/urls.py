from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from agenda.views import get_medico_availability

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('agenda/', include('agenda.urls')),
    path('api/medico/<int:medico_id>/availability/', get_medico_availability, name='medico_availability'),
]
