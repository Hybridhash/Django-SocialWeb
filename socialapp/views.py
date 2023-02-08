from django.shortcuts import render
from socialapp.forms import UserSignupForm
from django.http import HttpResponse
from django.template.context_processors import csrf
# This will let us get the HTML fragments from the back end
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import login

#Taking all the models from application
from .models import *




#View for index page, returned to HTML template
def index(request):
    profiles = Profile.objects.all()
    #response = "Hello" #Test Response 
    return render(request, 'socialapp/index.html', {'profiles': profiles})

def user_signup(request):
    if request.method == 'GET':
        context = {'form': UserSignupForm}
        return render(request,'socialapp/signup.html', context)
    elif request.method == 'POST':
        form = UserSignupForm(request.POST)
        #Checking form is valid
        if form.is_valid():
            # To commit new user to the data base
            user = form.save()
            # Session for user from django
            #login(request, user)
            return render(request,'socialapp/home.html')
        # context = {'form': form}
        # return render(request,'socialapp/signup.html', context)
        #     login(request, user)
        #     template = render(request, 'profile.html')
        #     template['Hx-Push'] = '/profile/'
        #     return template

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)
