from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('chat/', include('chat.urls'),name='chat-room'),
    path('admin/', admin.site.urls),
    path('auth/',include('users.urls')),
]
