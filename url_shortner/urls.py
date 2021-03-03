from django.urls import path
from . import views
urlpatterns = [
    path("",views.url_home,name="url_home"),
    path("<slug:slug>",views.url_redirect,name="url_redirect"),
]