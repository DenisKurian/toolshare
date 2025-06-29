from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin 

urlpatterns = [
     path('admin/', admin.site.urls),  # This registers the admin namespace
     path('SiteAdm/',include('SiteAdm.urls')),
     path('Guest/',include('Guest.urls')),
     path('',include('User.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
