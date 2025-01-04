from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from articles.views import Main
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view(), name='index'),
    path('users/', include('users.urls', namespace='users')),
    path('articles/', include('articles.urls', namespace='articles')),
    path('ai/', include('ai.urls', namespace='ai')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)