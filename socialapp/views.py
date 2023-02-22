from django.shortcuts import render, redirect, get_object_or_404
from socialapp.forms import UserSignupForm, UserLoginForm, UserProfileForm, PostForm
from django.views import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# This will let us get the HTML fragments from the back end
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import logging
from django.contrib.auth.decorators import login_required
from django.http import Http404

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


# @login_required(login_url="login/")
# def homepage(request):
#     return render(request=request, template_name="socialapp/home.html")


class Home(View):
    def get(self, request, *args, **kwargs):
        post_form = PostForm()
        # post_create = PostCreate.as_view(success_url=reverse_lazy("home"))
        # return post_create(request, *args, **kwargs)
        post_list = PostList.as_view()(request)

        return render(
            request=request,
            template_name="socialapp/home.html",
            context={
                "post_form": post_form,
                # "post_create_view": post_create,
                "post_list": post_list.context_data["post_list"],
            },
        )


@login_required(login_url="login/")
def user_logout(request):
    logout(request)
    return redirect("/login")


class UserProfileEdit(UpdateView):
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

    # user = User.objects.get(username=username)
    # if request.method == "POST":
    #     form = UserProfileForm(username, request.POST, instance=user)
    #     if form.is_valid():
    #         form.save()
    #         # do something with the updated user
    #         ...
    # else:
    #     form = UserProfileForm(username, instance=user)
    # return render(request, "socialapp/profile.html", {"profile_form_a": form})

    # model1 = Profile
    # fields = ["country", "birthdate", "image"]
    form_class = UserProfileForm
    # model2 = User
    # form_class = UserBaseForm

    template_name = "socialapp/profile_update.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user = User.objects.get(username=self.request.user.username)
        # logging.debug(get_object_or_404(Profile, user=user))
        profile = get_object_or_404(Profile, user=user)
        return Profile.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_form"] = self.get_form()
        logging.debug(context)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.image = self.request.FILES.get("image")
        return super().form_valid(form)


@login_required(login_url="login/")
def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        results = get_object_or_404(Profile, user__username=user)
        logging.debug(results)
        return render(request, "socialapp/profile.html", {"results": results})
    except Http404:
        url = reverse_lazy("profile_create")
        message = "Profile not found. Click here to create a profile:"
        return render(request, "socialapp/profile.html", {"error_message": message})


class UserProfileCreate(LoginRequiredMixin, CreateView):
    form_class = UserProfileForm
    template_name = "socialapp/profile_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.image = self.request.FILES.get("image")
        return super().form_valid(form)

    logging.debug(form_valid)


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    # template_name = "socialapp/post_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.image = self.request.FILES.get("image")
        return super().form_valid(form)

    logging.debug(form_valid)


class PostList(ListView):

    model = Post

    def get_queryset(self):
        user = User.objects.get(username=self.request.user.username)
        # logging.debug(get_object_or_404(Profile, user=user))
        return Post.objects.filter(owner=user)  # [:5] Get 5 books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = self.get_queryset()
        logging.debug(context)
        return context


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm

    template_name = "socialapp/post_update.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        qs = super().get_queryset()
        user = User.objects.get(username=self.request.user.username)
        # logging.debug(get_object_or_404(Profile, user=user))
        # profile = get_object_or_404(Profile, user=user)
        return qs.filter(owner=user, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_update"] = self.get_form()
        # logging.debug(context)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.image = self.request.FILES.get("image")
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    # form_class = PostForm

    template_name = "socialapp/post_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs["pk"], owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully.")
        logging.debug(messages.success(request, "Post deleted successfully."))
        return super().delete(request, *args, **kwargs)
