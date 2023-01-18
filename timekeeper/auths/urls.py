from django.urls import path
from . import views
from .views import PasswordsChangeView

app_name = "auths"

urlpatterns = [
    path("", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),
    path('password/', PasswordsChangeView.as_view(
        template_name='auths/change-password.html'), name="change_password"),
]
