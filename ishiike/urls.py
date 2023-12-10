from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('review.urls')),
    path('syllabus/', include('search_syllabus.urls')),
    path('sw.js', (TemplateView.as_view(template_name="sw.js",
    content_type='application/javascript', )), name='sw.js'),
    path('api/', include('api.urls')),
    path('welcome/', include('wiki.urls')),
    path('notifications/', include('django_nyt.urls')),
    path('qanda/', include('QandA.urls')),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)