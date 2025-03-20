from django.urls import path

from file_uploader import views

urlpatterns = [
    path("upload/", views.FileUploadAPIView.as_view(), name="file_upload"),
]
