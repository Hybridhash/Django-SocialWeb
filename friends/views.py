import logging
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q, OuterRef, Subquery
from socialapp.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FriendRequest
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View


# Create your views here.
class FriendHome(LoginRequiredMixin, TemplateView):
    """
    Template Class View:  To show friends, friends request and search on home page
    """

    template_name = "friends/friend_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_list = FriendSearch.as_view()(self.request)
        context["friend_list"] = friend_list.context_data["object_list"]

        # Get the list of requests received
        friend_requests_received = FriendRequest.objects.filter(to_user=self.request.user, accepted=False)

        # Get the list of friends where request is accepted
        friends_circle = FriendRequest.objects.filter(
            from_user=self.request.user, accepted=True
        ) | FriendRequest.objects.filter(to_user=self.request.user.id, accepted=True)

        logging.debug(friends_circle)
        context["friend_requests_received"] = friend_requests_received
        context["friends_circle"] = friends_circle

        return context


class FriendSearch(LoginRequiredMixin, ListView):
    """
    List Class View:  To show friends available on submitting the search query
    """

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

            queryset = queryset.annotate(
                is_friend=Subquery(friend_requests_sent.filter(to_user=OuterRef("pk"), accepted=1).values("id")[:1]),
                is_pending=Subquery(friend_requests_sent.filter(to_user=OuterRef("pk"), accepted=0).values("id")[:1]),
            )

        else:
            queryset = User.objects.none()

        return queryset


class FriendCreate(LoginRequiredMixin, CreateView):
    """
    Create Class View:  To create new friends request on submitting the request button
                        It displays message in case if there is already pending request
    """

    model = FriendRequest
    fields = []
    success_url = reverse_lazy("friends")

    def form_valid(self, form):
        from_user = self.request.user
        to_user = get_object_or_404(User, pk=self.kwargs["pk"])
        if from_user != to_user:
            if FriendRequest.objects.filter(
                Q(from_user=from_user, to_user=to_user) | Q(from_user=to_user, to_user=from_user)
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
                messages.success(self.request, "Friend request sent to {}".format(to_user.username))
        return redirect(reverse_lazy("friends"))


class FriendAccept(View):
    """
    Class View: Show friends request and button to accept it
    """

    template_name = "friends/friend_home.html"

    def post(self, request, *args, **kwargs):
        friend_request = get_object_or_404(FriendRequest, pk=self.kwargs["pk"])
        friend_request.accepted = True
        friend_request.save()
        messages.success(self.request, "Friend request accepted")
        return redirect(reverse_lazy("friends"))


class FriendDelete(LoginRequiredMixin, View):
    """
    Class View: to delete the friends
    """

    template_name = "friends/friend_home.html"

    def post(self, request, *args, **kwargs):
        friend_request = get_object_or_404(FriendRequest, pk=self.kwargs["pk"])
        friend_request.delete()
        messages.warning(self.request, "Friend deleted")
        return redirect(reverse_lazy("friends"))
