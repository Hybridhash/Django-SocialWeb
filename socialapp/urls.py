from django.urls import include, path
from . import views
#Importing the API's
#from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.user_signup, name='signup'),
]