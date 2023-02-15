from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PasswordsChangeView, PasswordsResetView

app_name = "auths"

urlpatterns = [
    path("", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),
    path("delete_user/<int:user_id>", views.delete_user, name="delete_user"),
    path('change-password/', PasswordsChangeView.as_view(
        template_name='auths/change-password.html'), name="change_password"),
    path('reset-password/', PasswordsResetView.as_view(
        template_name='auths/change-password.html'), name="password_reset"),
    path('reset-password-success/', views.reset_password_success,
         name="password_reset_success"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auths/change-password-form.html'), name="password_reset_confirm"),
    path('reset/done/', views.reset_password_complete,
         name="password_reset_complete"),
]
