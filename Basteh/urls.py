from django.urls import path, include 
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('mositafan_admin_billigpost/', admin.site.urls), # change admin something different for security
    path('api/v1/account/', include('account.urls')),
    path('api/v1/advertise/', include('advertise.urls')),
    path('api/v1/chat/', include('chat.urls')),
    path('api/v1/payment/', include('payment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

admin.site.site_header = "Basteh"
