from django.urls import path
from .views import upload_file, list_lifters, lifter_detail, list_meets, meet_results, download_meet_results


urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('lifters/', list_lifters, name='list_lifters'),
    path('lifters/<int:lifter_id>/', lifter_detail, name='lifter_detail'),
    path('meets/', list_meets, name='list_meets'),
    path('<int:meet_id>/results/', meet_results, name='meet_results'),
    path('<int:meet_id>/results/download/', download_meet_results, name='download_meet_results'),

]
