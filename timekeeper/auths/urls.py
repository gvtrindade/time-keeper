from django.urls import path
from . import views

app_name = "auths"

urlpatterns = [
  path('', views.login_user, name='login'),
  path('logout', views.logout_user, name='logout')
]