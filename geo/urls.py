from django.urls import path

from .views import GeoCountriesView, GeoLanguagesView

urlpatterns = [
    path('languages/', GeoLanguagesView.as_view()),
    path('countries/', GeoCountriesView.as_view()),
]
