from django.urls import path
from csvconverter import views

urlpatterns = [
    path('csvupload/', views.CsvUploadView, name='csvupload'),
]
