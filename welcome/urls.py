from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'welcome'

urlpatterns = [
    #path('_accounts/sign-up/', views.SignUpView2.as_view(), name='account_signup'),
    path('admin/', admin.site.urls),
    path('notifications/', include('django_nyt.urls')),
]

if settings.DEBUG:    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

