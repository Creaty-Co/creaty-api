from django.urls import path

from .views import *

urlpatterns = [
    path('', TagsView.as_view()),
    path('categories/', TagsCategoriesView.as_view())
]
