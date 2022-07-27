from django.conf import settings
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('main/', PagesMainView.as_view()),
    path('main/mentors/<int:mentor_id>/', PagesMainMentorView.as_view()),
    path('personal/<str:shortcut>/', PagesPersonalView.as_view()),
    path(
        'personal/<str:shortcut>/mentors/<int:mentor_id>/',
        PagesPersonalMentorView.as_view(),
    ),
    path('faqs/', PagesFaqsView.as_view()),
    path('faqs/<int:id>/', PagesFaqView.as_view()),
    path('links/socials/', PagesLinksSocialsView.as_view()),
    path('links/socials/<int:id>/', PagesLinksSocialView.as_view()),
    path('links/documents/', PagesLinksDocumentsView.as_view()),
    path('links/documents/<int:id>/', PagesLinksDocumentView.as_view()),
    re_path(
        f'locales/(?P<language>{"|".join(l[0] for l in settings.LANGUAGES)})'
        f'/translation.json/',
        PagesLocaleView.as_view(),
    ),
]
