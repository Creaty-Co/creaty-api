from django.urls import path

from .views import *

urlpatterns = [
    path('main/', PagesMainView.as_view()),
    path('personal/<str:shortcut>/', PagesPersonalView.as_view()),
    path('faqs/', PagesFaqsView.as_view()),
    path('faqs/<int:id>/', PagesFaqView.as_view())
]
