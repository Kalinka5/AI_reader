from django.urls import path
from . import views

urlpatterns = [
    path('upload-pdf', views.upload_pdf, name='upload_pdf'),
    path('ai-assistent', views.ai_assistent, name='ai_assistent'),
]
