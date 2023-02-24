import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q, OuterRef, Subquery
from socialapp.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FriendRequest
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.db.models import Case, When, BooleanField

# Create your views here.


class FriendHome(TemplateView):
    template_name = "friends/friend_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_list = FriendSearch.as_view()(self.request)
        context["friend_list"] = friend_list.context_data["object_list"]

        # Get the list of requests received
        friend_requests_received = FriendRequest.objects.filter(
            to_user=self.request.user, accepted=False
        )

        # Get the list of friends where request is accepted
        friends_circle = FriendRequest.objects.filter(
            from_user=self.request.user, accepted=True
        ) or FriendRequest.objects.filter(to_user=self.request.user, accepted=True)

        logging.debug(friends_circle)
        context["friend_requests_received"] = friend_requests_received
        context["friends_circle"] = friends_circle

        return context


class FriendSearch(ListView):
    model = User
    template_name = "friends/friend_home.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            queryset = User.objects.filter(
                # return User.objects.filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )

            friend_requests_sent = FriendRequest.objects.filter(
                from_user=self.request.user, to_user__in=queryset
            ).values("to_user")

            friend_requests_received = FriendRequest.objects.filter(
                from_user__in=queryset, to_user=self.request.user
            ).values("from_user")

            queryset = queryset.annotate(
                is_friend=Subquery(
                    friend_requests_sent.filter(
                        to_user=OuterRef("pk"), accepted=1
                    ).values("id")[:1]
                ),
                is_pending=Subquery(
                    friend_requests_sent.filter(
                        to_user=OuterRef("pk"), accepted=0
                    ).values("id")[:1]
                ),
            )

        else:
            queryset = User.objects.none()

        return queryset


class FriendCreate(LoginRequiredMixin, CreateView):
    model = FriendRequest
    fields = []
    success_url = reverse_lazy("friends")

    def form_valid(self, form):
        from_user = self.request.user
        to_user = get_object_or_404(User, pk=self.kwargs["pk"])
        if from_user != to_user:
            if FriendRequest.objects.filter(
                Q(from_user=from_user, to_user=to_user)
                | Q(from_user=to_user, to_user=from_user)
            ).exists():
                messages.warning(
                    self.request,
                    "Friend request already exists against {}".format(to_user.username),
                )
            else:
                friend_request = form.save(commit=False)
                friend_request.from_user = from_user
                friend_request.to_user = to_user
                friend_request.save()
                messages.success(
                    self.request, "Friend request sent to {}".format(to_user.username)
                )
        return redirect(reverse_lazy("friends"))


class FriendAccept(TemplateView):
    # model = FriendRequest
    # fields = ["accepted"]
    # success_url = reverse_lazy("friends")

    # def form_valid(self, form):
    #     form.is_valid()
    #     friend_request = get_object_or_404(FriendRequest, pk=self.kwargs["pk"])
    #     logging.debug(friend_request)
    #     friend_request.accepted = True
    #     friend_request.save()
    #     logging.debug(friend_request.save())
    #     return super().form_valid(form)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     friend_request = get_object_or_404(FriendRequest, pk=self.kwargs["pk"])
    #     context["friend_request"] = friend_request
    #     return context
    template_name = "friends/friend_home.html"

    success_url = reverse_lazy("friends")

    def post(self, request, *args, **kwargs):
        friend_request = get_object_or_404(FriendRequest, pk=self.kwargs["pk"])
        friend_request.accepted = True
        friend_request.save()
        return redirect(reverse_lazy("friends"))
