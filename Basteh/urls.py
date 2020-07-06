from django.urls import path, include 
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls), # change admin something different for security
    path('api/v1/account/', include('account.urls')),
    path('api/v1/advertise/', include('advertise.urls')),
    path('api/v1/blog/', include('blog.urls')),
    path('api/v1/chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

admin.site.site_header = "Basteh"
