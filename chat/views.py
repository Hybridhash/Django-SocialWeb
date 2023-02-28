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
        # slug = self.kwargs.get("slug")
        rooms = ChatSpace.objects.all()  # get all rooms
        context["rooms"] = rooms
        return context


# class SpaceCreateView(TemplateView):
#     template_name = "chat/space_create.html"

#     def post(self, request, *args, **kwargs):
#         space_name = request.POST["space_name"]
#         # Unique identification string (uid) using random letters and digits
#         uid = str("".join(random.choices(string.ascii_letters + string.digits, k=4)))
#         # To store a A URL slug
#         space_slug = slugify(space_name + "_" + uid)
#         # ChatSpace object using the name and slug attributes and saves it to the database
#         space = ChatSpace.objects.create(name=space_name, slug=space_slug)
#         return redirect(reverse("chat_space", kwargs={"slug": space.slug}))

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)


# class SpaceJoinView(TemplateView):
#     template_name = "chat/space_join.html"

#     def post(self, request, *args, **kwargs):
#         space_slug = request.POST["space_slug"]
#         space = ChatSpace.objects.get(slug=space_slug)
#         return redirect(reverse("chat_space", kwargs={"slug": space.slug}))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


# class ChatSpace(TemplateView):

#     template_name = "chat/chat_space.html"

#     # def get_context_data(self, **kwargs):
#     # context = super().get_context_data(**kwargs)
#     # return render(self.request, "chat/chat_space.html", {"space_name": space_name})
#     def get(self, request, *args, **kwargs):
#         space_name = self.kwargs.get("room_name")
#         return render(request, self.template_name, {"room_name": space_name})


class ChatRoom(TemplateView):
    template_name = "chat/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["name"] = get_object_or_404(ChatSpace, slug=slug).name
        context["slug"] = self.kwargs["slug"]
        return context

    # room = ChatSpace.objects.get(slug=slug)
    # return render(request, "chat/room.html", {"name": room.name, "slug": room.slug})


class RoomCreate(TemplateView):

    template_name = "chat/create.html"

    def post(self, request, *args, **kwargs):
        space_name = request.POST["room_name"]
        # Unique identification string (uid) using random letters and digits
        uid = str("".join(random.choices(string.ascii_letters + string.digits, k=4)))
        # To store a A URL slug (Act as a unique identifier for rooms)
        space_slug = slugify(space_name + "_" + uid)
        # ChatSpace object using the name and slug attributes and saves it to the database
        space = ChatSpace.objects.create(name=space_name, slug=space_slug)
        return redirect(reverse("chat", kwargs={"slug": space.slug}))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    # if request.method == "POST":
    #     room_name = request.POST["room_name"]
    #     uid = str("".join(random.choices(string.ascii_letters + string.digits, k=4)))
    #     room_slug = slugify(room_name + "_" + uid)
    #     room = ChatSpace.objects.create(name=room_name, slug=room_slug)
    #     return redirect(reverse("chat", kwargs={"slug": room.slug}))
    # else:
    #     return render(request, "chat/create.html")


class SpaceJoin(TemplateView):

    template_name = "chat/join.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def post(self, request, *args, **kwargs):
        space_slug = request.POST["space_name"]
        space = ChatSpace.objects.get(slug=space_slug)
        return redirect(reverse("chat", kwargs={"slug": space.slug}))

    # if request.method == "POST":
    #     room_name = request.POST["room_name"]
    #     room = ChatSpace.objects.get(slug=room_name)
    #     return redirect(reverse("chat", kwargs={"slug": room.slug}))
    # else:
    #     return render(request, "chat/join.html")
