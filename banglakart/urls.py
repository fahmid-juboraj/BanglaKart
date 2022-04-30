from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
admin.site.site_header = 'BanglaKart Admin Panel'  
admin.site.index_title = 'Features area' 
admin.site.site_title = 'BanglaCart_Admin'

urlpatterns = [
    path('admin/',admin.site.urls),
    path('store/',include('store.urls')),
    path('cart/', include('carts.urls')),    
    path('accounts/', include('accounts.urls')),
    path("",views.home,name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
