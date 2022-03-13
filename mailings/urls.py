from django.urls import path

from .views import *

urlpatterns = [
    path('subscribe/', MailingsSubscribeView.as_view()),
    path('unsubscribe/<str:uuid>/', MailingsUnsubscribeView.as_view()),
    path('', MailingsView.as_view()),
    path('<int:id>/', MailingView.as_view()),
    path('<int:id>/send/', MailingSendView.as_view()),
    path('subscribers/xlsx/', MailingsSubscribersXlsxView.as_view())
]
