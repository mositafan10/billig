from django.urls import path, include 
from django.contrib import admin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/advertise/', include('advertise.urls')),
    path('api/v1/blog/', include('blog.urls')),
    path('api/v1/chat/', include('chat.urls')),
]

admin.site.site_header = "Basteh"
