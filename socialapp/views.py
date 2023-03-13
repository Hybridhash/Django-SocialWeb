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
from django.contrib import messages
import logging
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Taking all the models from application
from .models import Post, Profile, User


def index(request):
    """
    GET Request: Render the landing page
    """
    return render(request, "socialapp/index.html")


def user_signup(request):
    """
    GET/POST Request: User Signup form for new registration
    """
    if request.method == "GET":
        context = {"form": UserSignupForm}
        return render(request, "socialapp/signup.html", context)
    elif request.method == "POST":
        form = UserSignupForm(request.POST)
        # Checking form is valid
        if form.is_valid():
            # To commit new user to the data base
            user = form.save()
            return redirect("/login")
        # Validate a crispy-form through AJAX to re-render any resulting form errors
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)


def user_login(request):
    """
    GET/POST Request: User Signup form for new registration
    """
    logging.debug("user_login called")
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
def user_logout(request):
    """
    GET Request: User request to logout from the session using builtin logout function
    """
    logout(request)
    return redirect("/login")


class Home(View):
    """
    Class View: User main landing page showing Post form and Post List
    """

    def get(self, request, *args, **kwargs):
        post_form = PostForm()
        post_list = PostList.as_view()(request)

        return render(
            request=request,
            template_name="socialapp/home.html",
            context={"post_form": post_form, "post_list": post_list.context_data["post_list"]},
        )


@login_required(login_url="login/")
def user_profile(request, username):
    """
    GET Request: To get the user profile while passing the username
                 User's have keep the profile blank and create it at later stage
    """
    try:
        user = User.objects.get(username=username)
        results = get_object_or_404(Profile, user__username=user)
        logging.debug(results)
        return render(request, "socialapp/profile.html", {"results": results})
    except Http404:
        url = reverse_lazy("profile_create")
        message = "Profile not found. Click here to create a profile:"
        return render(request, "socialapp/profile.html", {"error_message": message})


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    """
    Update Class View:  View to update the user profile
    """

    form_class = UserProfileForm
    template_name = "socialapp/profile_update.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user = User.objects.get(username=self.request.user.username)
        # logging.debug(get_object_or_404(Profile, user=user))
        return Profile.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_form"] = self.get_form()
        logging.debug(context)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        if "image" in self.request.FILES:
            form.instance.image = self.request.FILES.get("image")
        return super().form_valid(form)


class UserProfileCreate(LoginRequiredMixin, CreateView):
    """
    Create Class View:  Enable the user to create a new profile after registration
                        User's have keep the profile blank and create it at later stage
    """

    form_class = UserProfileForm
    template_name = "socialapp/profile_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.image = self.request.FILES.get("image")
        return super().form_valid(form)

    logging.debug(form_valid)


class PostCreate(LoginRequiredMixin, CreateView):
    """
    Create Class View: Enables the user to create new post
    """

    form_class = PostForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.image = self.request.FILES.get("image")
        return super().form_valid(form)

    logging.debug(form_valid)


class PostList(LoginRequiredMixin, ListView):
    """
    List Class View: List the post submitted by user
    """

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


class PostUpdate(LoginRequiredMixin, UpdateView):
    """
    Update Class View: Update the user posts from the database
    """

    model = Post
    form_class = PostForm
    template_name = "socialapp/post_update.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        qs = super().get_queryset()
        user = User.objects.get(username=self.request.user.username)
        return qs.filter(owner=user, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_update"] = self.get_form()
        # logging.debug(context)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        if "image" in self.request.FILES:
            form.instance.image = self.request.FILES.get("image")
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):
    """
    Delete Class View: Delete the user posts from the data base
    """

    model = Post
    template_name = "socialapp/post_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs["pk"], owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully.")
        logging.debug(messages.success(request, "Post deleted successfully."))
        return super().delete(request, *args, **kwargs)
