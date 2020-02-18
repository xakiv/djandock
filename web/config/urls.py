from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]

# On ajoute les urls d'appli en autant de sous-domaines qu'il y a d'appli
for app in settings.OUR_APPS:
    urlpatterns.insert(
        1,
        path('{}/'.format(app), include('{}.urls'.format(app), namespace=app)),
    )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
