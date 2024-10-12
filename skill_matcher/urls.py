"""
URL configuration for skill_matcher project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [

	path('admin/', admin.site.urls),

	##### user related path########################## 
	path('', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),

]
