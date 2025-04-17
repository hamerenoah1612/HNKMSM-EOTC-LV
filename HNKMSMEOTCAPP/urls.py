from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static  
from django.conf import settings  
from django.contrib.auth.views import LoginView
# from users.views import custom_confirm_email  # your view is in users/views.py

 
urlpatterns = [
    # Admin
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    
    # User Management
    path('account/', include('users.urls')),
    path('account/', include('allauth.urls')),
    
    
    path('', include('pages.urls')),
    path('projectVote/', include('projectVote.urls')),
    path('services/', include('services.urls')),
    path('schools/', include('schools.urls')),
    path('members/', include('members.urls')),
    path('events/', include('events.urls')),
    path('multimedia/', include('multimedia.urls')),
    path('blog/', include('blog.urls')),
    path('marriage/', include('marriage.urls')),
    path('payments/', include('payments.urls')),
    path('shopProducts/', include('shopProducts.urls')),
    path('massaging/', include('massaging.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    
