from django.urls import path

from .views import FormApplicationsView, FormsApplicationsXlsxView, FormsView, FormView

urlpatterns = [
    path('', FormsView.as_view()),
    path('<int:id>/', FormView.as_view()),
    path('<int:form_id>/applications/', FormApplicationsView.as_view()),
    path('applications/xlsx/', FormsApplicationsXlsxView.as_view()),
]
