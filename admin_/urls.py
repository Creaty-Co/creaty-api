from django.urls import path

from .views import *

urlpatterns = [
    path('mentors/', AdminMentorsView.as_view()),
    path('categories/', AdminCategoriesView.as_view())
]
