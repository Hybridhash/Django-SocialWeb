from django.shortcuts import render

# Create your views here.

#Taking all the models from protein app
from .models import *

#View for protein data, returned to HTML template
def index(request):
    profiles = Profile.objects.all()
    #response = "Hello" #Test Response 
    return render(request, 'socialapp/index.html', {'users': profiles}) 