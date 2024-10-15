from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Review

class CustomUserAdmin(UserAdmin):
    """Custom User Admin to manage CustomUser model."""
    model = CustomUser
    list_display = ('email', 'name', 'is_staff', 'is_active')  # Fields to display in the admin list view
    list_filter = ('is_staff', 'is_active')  # Filters for the admin list view
    search_fields = ('email', 'name')  # Searchable fields in the admin interface
    ordering = ('email',)  # Default ordering for the admin list view

class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for managing reviews."""
    list_display = ('movie_title', 'rating', 'user', 'created_date')  # Fields to display in the admin list view
    list_filter = ('rating', 'created_date')  # Filters for the admin list view
    search_fields = ('movie_title', 'content')  # Searchable fields in the admin interface
    ordering = ('-created_date',)  # Default ordering for the admin list view

# Registering the models with their respective admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Review, ReviewAdmin)
