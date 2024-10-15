"""
URL configuration for movie_review_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reviews.views import home  # Import your new view
from rest_framework.routers import DefaultRouter
from reviews.views import ReviewViewSet

urlpatterns = [
    path('', home, name='home'),  # Add this line for the root URL
    path('admin/', admin.site.urls),  # Admin site URL
    path('api/', include('reviews.urls')),  # Include all routes from the app-level urls
]
