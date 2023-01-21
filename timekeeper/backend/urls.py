from django.urls import path
from . import views

app_name = "backend"

urlpatterns = [
    path("", views.index, name="index"),
    path("history", views.history, name="history"),
    path("include", views.include, name="include"),
    path("users", views.user_list, name="userList"),
    path("users/<int:user_id>", views.user, name="user"),
    path("delete_record/<int:record_id>",
         views.delete_record, name="delete_record"),
]
