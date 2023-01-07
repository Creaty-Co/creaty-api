from django.urls import path

from .views import AdminMentorsView

urlpatterns = [path('mentors/', AdminMentorsView.as_view())]
