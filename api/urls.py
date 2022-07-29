import mimetypes

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.response import Response
# noinspection PyPackageRequirements
from silk.profiling.profiler import silk_profile

from base.views import BaseView

mimetypes.add_type('application/javascript', '.js')


class CalcView(BaseView):
    @silk_profile(name='name')
    def get(self, request):
        i = 0
        max_i = int(request.query_params['a'])
        while i < max_i:
            i += 1
        return Response(i)


urlpatterns = [
    path('__docs__/', SpectacularAPIView.as_view(), name='__docs__'),
    path('', SpectacularSwaggerView.as_view(url_name='__docs__')),
    path('silk/', include('silk.urls', namespace='silk')),
    path('django_admin/', admin.site.urls),
    path('base/', include('base.urls')),
    path('account/', include('account.urls')),
    path('admin/', include('admin_.urls')),
    path('mentors/', include('mentors.urls')),
    path('tags/', include('tags.urls')),
    path('forms/', include('forms.urls')),
    path('mailings/', include('mailings.urls')),
    path('pages/', include('pages.urls')),
    path('geo/', include('geo.urls')),
    path('calc/', CalcView.as_view()),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
