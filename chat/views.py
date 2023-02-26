from django.shortcuts import render

# Create your views here.


def chat_home(request):
    return render(request, "chat/chat_home.html")


def chat_space(request):
    return render(request, "chat/chat_space.html", {"space_name": space_name})
