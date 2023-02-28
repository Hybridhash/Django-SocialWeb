from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render, reverse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .models import ChatSpace, ChatMessage
import random
import string
from django.contrib.auth.decorators import login_required

# Create your views here.


class ChatHome(TemplateView):

    template_name = "chat/chat_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = ChatSpace.objects.all()  # get all rooms
        context["rooms"] = rooms
        return context


class ChatRoom(TemplateView):
    template_name = "chat/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["name"] = get_object_or_404(ChatSpace, slug=slug).name
        context["slug"] = self.kwargs["slug"]

        space_messages = ChatMessage.objects.filter()
        return context


class SpaceCreate(TemplateView):

    template_name = "chat/create.html"

    def post(self, request, *args, **kwargs):
        space_name = request.POST["space_name"]
        # Unique identification string (uid) using random letters and digits
        uid = str("".join(random.choices(string.ascii_letters + string.digits, k=4)))
        # To store a A URL slug (Act as a unique identifier for rooms)
        space_slug = slugify(space_name + "_" + uid)
        # ChatSpace object using the name and slug attributes and saves it to the database
        space = ChatSpace.objects.create(name=space_name, slug=space_slug)
        return redirect(reverse("chat", kwargs={"slug": space.slug}))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SpaceJoin(TemplateView):

    template_name = "chat/join.html"

    def post(self, request, *args, **kwargs):
        space_slug = request.POST["space_name"]
        space = ChatSpace.objects.get(slug=space_slug)
        return redirect(reverse("chat", kwargs={"slug": space.slug}))
