from django.shortcuts import render, redirect
from socialapp.forms import UserSignupForm, UserLoginForm
from django.http import HttpResponse
from django.template.context_processors import csrf

# This will let us get the HTML fragments from the back end
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import logging
from django.contrib.auth.decorators import login_required

# Taking all the models from application
from .models import *


# View for index page, returned to HTML template
def index(request):
    profiles = Profile.objects.all()
    # response = "Hello" #Test Response
    return render(request, "socialapp/index.html", {"profiles": profiles})


def user_signup(request):
    logging.debug(request)
    if request.method == "GET":
        context = {"form": UserSignupForm}
        return render(request, "socialapp/signup.html", context)
    elif request.method == "POST":
        form = UserSignupForm(request.POST)
        # Checking form is valid
        if form.is_valid():
            # To commit new user to the data base
            user = form.save()
            # Session for user from django
            # login(request, user)
            template = render(request, "socialapp/home.html")
            template["HX-Push"] = "/home/"
            return template

        # Validate a crispy-form through AJAX to re-render any resulting form errors
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)


def user_login(request):
    logging.debug("user_login called")
    logging.debug(request)
    if request.user.is_authenticated:
        logging.debug("user authentication called")
        return redirect("/home")

    else:
        next = request.GET.get("next")
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect("/home")

        context = {
            "login_form": form,
        }
        return render(request, "socialapp/login.html", context)


@login_required(login_url="login/")
def homepage(request):
    return render(request=request, template_name="socialapp/home.html")


@login_required(login_url="login/")
def user_logout(request):
    logout(request)
    return redirect("/login")
