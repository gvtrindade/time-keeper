from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),
    path('auths/', include('django.contrib.auth.urls')),
    path('auths/', include('auths.urls'))
]
