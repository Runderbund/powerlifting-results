from django.urls import path
from .views import upload_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    # path('success/', views.upload_success, name='upload_success'),
    # Not using a separate page for now. May later.
]
