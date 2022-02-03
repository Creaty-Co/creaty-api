from django.urls import path

from .views import *

urlpatterns = [
    path('', FormsView.as_view()),
    path('<int:form_id>/applications/', FormApplicationsView.as_view())
]
