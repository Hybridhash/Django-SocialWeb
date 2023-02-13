from django.shortcuts import render, redirect
from socialapp.forms import (
    UserSignupForm,
    UserLoginForm,
    UserProfileCombinedForm,
    UserProfileForm,
)
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
            # template = render(request, "socialapp/login.html")
            # template["HX-Push"] = "/login/"
            # return template
            return redirect("/login")
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


def user_profile_edit(request, username):
    # if request.method == "GET":
    #     context = {
    #         "profile_form_a": UserProfileAForm,
    #         "profile_form_b": UserProfileBForm,
    #     }
    #     return render(request, "socialapp/profile.html", context)

    # elif request.method == "POST":
    #     form = UserProfileCombinedForm(request.POST)
    #     if form.is_valid():
    #         form_a = form.cleaned_data["profile_a"]
    #         form_a.save()
    #         form_b = form.cleaned_data["profile_b"]
    #         form_b.save()
    #         return redirect("success_url")
    # user = User.objects.get(username=username)
    # if request.method == "POST":
    #     form = UserProfileCombinedForm(username, request.POST, instance=user)
    #     if form.is_valid():
    #         form.save()
    #         # do something with the updated user
    #         ...
    # else:
    #     form = UserProfileCombinedForm(username, instance=user)
    # return render(request, "socialapp/profile.html", {"profile_form_a": form})
    # # return render(request, "socialapp/profile.html", {"username": username})

    user = User.objects.get(username=username)
    if request.method == "POST":
        form = UserProfileForm(username, request.POST, instance=user)
        if form.is_valid():
            form.save()
            # do something with the updated user
            ...
    else:
        form = UserProfileForm(username, instance=user)
    return render(request, "socialapp/profile.html", {"profile_form_a": form})


@login_required(login_url="login/")
def user_profile(request, username):
    user = User.objects.get(username=username)
    results = Profile.objects.get(user__username=user)
    logging.debug(results)
    return render(request, "socialapp/profile.html", {"results": results})
