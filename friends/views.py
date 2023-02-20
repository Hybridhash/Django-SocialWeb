import logging
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from socialapp.models import User

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_list"] = self.get_queryset()
        logging.debug(context)
        return context


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
