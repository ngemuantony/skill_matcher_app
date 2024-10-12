from django.urls import path
from . import views  # Import your views module

urlpatterns = [
    path('job-list/', views.job_list, name='job_list'),  # Ensure this pattern exists
    path('job-search/', views.job_search, name='job_search'),
]
