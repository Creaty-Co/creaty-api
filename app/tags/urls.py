from django.urls import path

from .views import (
    TagsCategoriesView,
    TagsCategoryTagsView,
    TagsCategoryView,
    TagsView,
    TagView,
)

urlpatterns = [
    path('', TagsView.as_view()),
    path('<int:id>/', TagView.as_view()),
    path('categories/', TagsCategoriesView.as_view()),
    path('categories/<int:id>/', TagsCategoryView.as_view()),
    path('categories/<category_id>/tags/', TagsCategoryTagsView.as_view()),
]
