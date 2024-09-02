from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('users.urls', namespace='users')),
    path('api/v1/friends/', include('friends.urls', namespace='friends')),
]
