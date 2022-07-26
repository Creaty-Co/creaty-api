from django.urls import path

from .views import *

urlpatterns = [path('mentors/', AdminMentorsView.as_view())]
