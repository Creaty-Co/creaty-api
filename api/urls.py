import mimetypes

import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

mimetypes.add_type('application/javascript', '.js')

urlpatterns = [
    path('__docs__/', SpectacularAPIView.as_view(), name='__docs__'),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', SpectacularSwaggerView.as_view(url_name='__docs__')),
    path('django_admin/', admin.site.urls),
    
    path('base/', include('base.urls')),
    path('account/', include('account.urls')),
    
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
