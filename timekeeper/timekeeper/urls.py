from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),
    path('auths/', include('auths.urls')),
    path('auths/', include('django.contrib.auth.urls')),
]

handler404 = 'backend.views.handler404'
handler403 = 'backend.views.handler403'
handler500 = 'backend.views.handler500'
