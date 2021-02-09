from django.urls import path
from . import views

urlpatterns = [
    path('execute/', views.LexxerExecuteView.as_view(), name='lex-execute'),
]
