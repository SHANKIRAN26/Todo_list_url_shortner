from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    # path("<int:id>", views.youtubers_detail, name="youtubers_detail"),
    path("edit/<int:id>",views.edit,name="edit"),
    path("delete/<int:id>",views.delete,name="delete"),
]