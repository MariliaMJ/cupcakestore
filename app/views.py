from django.shortcuts import render
from .models import Cupcake

def get_cupcakes(request):
    cupcakes = Cupcake.objects.all()
    return render(request, 'list.html', {'cupcakes': cupcakes})
# Create your views here.
