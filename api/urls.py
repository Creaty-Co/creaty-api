import mimetypes
import re

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

mimetypes.add_type('application/javascript', '.js')

urlpatterns = []

if settings.USE_BROWSABLE_API:
    urlpatterns += [
        path('__docs__/', SpectacularAPIView.as_view(), name='__docs__'),
        path('', SpectacularSwaggerView.as_view(url_name='__docs__')),
    ]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('base/', include('app.base.urls')),
    path('users/', include('app.users.urls')),
    path('mentors/', include('app.mentors.urls')),
    path('tags/', include('app.tags.urls')),
    path('forms/', include('app.forms.urls')),
    path('mailings/', include('app.mailings.urls')),
    path('pages/', include('app.pages.urls')),
    path('geo/', include('app.geo.urls')),
    path('bookings/', include('app.bookings.urls')),
    path('calcom/', include('app.calcom.urls')),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


def _make_optional_slash(url_pattern_or_resolver):
    match url_pattern_or_resolver:
        case URLResolver():
            url_pattern_or_resolver: URLResolver
            for child in url_pattern_or_resolver.url_patterns:
                _make_optional_slash(child)
        case URLPattern():
            url_pattern_or_resolver.pattern.regex = re.compile(
                re.sub(
                    r'/(?=[\\Z$]|$)',
                    '/?',
                    url_pattern_or_resolver.pattern.regex.pattern,
                )
            )


for url_pattern in urlpatterns:
    _make_optional_slash(url_pattern)
