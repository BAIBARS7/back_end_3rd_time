from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewViewSet,
    UserViewSet,
    ReviewByMovieView,
    ReviewSearchView,
    CustomAuthToken,
    SignupView  # Import your new SignupView
)
from django.contrib.auth import views as auth_views  # Import Django's built-in auth views

# Create a router and register the ViewSets with it
router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)  # Registering ReviewViewSet for managing reviews
router.register(r'users', UserViewSet)  # Registering UserViewSet for user management

urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the router under the root of 'api/'
    
    # Endpoints for specific functionalities
    path('reviews/movie/<str:title>/', ReviewByMovieView.as_view(), name='reviews-by-movie'),  # Endpoint to view reviews by movie title
    path('reviews/search/', ReviewSearchView.as_view(), name='review-search'),  # Endpoint to search reviews
    
    # Authentication endpoints
    path('login/', CustomAuthToken.as_view(), name='login'),  # Endpoint for user login
    path('logout/', CustomAuthToken.as_view(), name='logout'),  # Logout endpoint (use appropriate view)
    
    # New signup endpoint
    path('signup/', SignupView.as_view(), name='signup'),  # Endpoint for user registration

    # Template rendering endpoints for authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Custom login template
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view (uses default)
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),  # Password reset view
]
