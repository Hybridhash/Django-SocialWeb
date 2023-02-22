import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from socialapp.models import User
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FriendRequest
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.


class Friends(ListView):
    # def get(self, request, *args, **kwargs):
    #     post_form = PostForm()
    #     # post_create = PostCreate.as_view(success_url=reverse_lazy("home"))
    #     # return post_create(request, *args, **kwargs)
    #     post_list = PostList.as_view()(request)

    #     return render(
    #         request=request,
    #         template_name="socialapp/home.html",
    #         context={
    #             "post_form": post_form,
    #             # "post_create_view": post_create,
    #             "post_list": post_list.context_data["post_list"],
    #         },
    #     )
    model = User
    template_name = "friends/friend_home.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return User.objects.filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )
        else:
            return User.objects.none()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["user_list"] = self.get_queryset()
    #     # logging.debug(context)
    #     return context


# class UserSearch(ListView):
#     model = User
#     template_name = "user_search.html"

#     def get_queryset(self):
#         query = self.request.GET.get("q")
#         if query:
#             return User.objects.filter(
#                 Q(username__icontains=query)
#                 | Q(first_name__icontains=query)
#                 | Q(last_name__icontains=query)
#             )
#         else:
#             return User.objects.none()


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

        # # return redirect("user_detail", pk=to_user.pk)
        # message = f"Friend request is send to a {to_user.username}"
        # return redirect(self.request, "friends/friend_home.html", {"message": message})
