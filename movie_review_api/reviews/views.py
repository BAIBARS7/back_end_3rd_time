from rest_framework import viewsets, permissions, generics
from .models import Review, CustomUser
from .serializers import ReviewSerializer, CustomUserSerializer, UserSerializer  # Import UserSerializer for signup
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.authtoken.models import Token

class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing movie reviews."""
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can manage reviews

    def perform_create(self, serializer):
        """Save the review with the current user as the author."""
        user = self.request.user
        serializer.save(user=user)

    def destroy(self, request, *args, **kwargs):
        """Delete a review instance."""
        review = self.get_object()
        if review.user != request.user:
            return Response({'error': 'You do not have permission to delete this review.'}, status=status.HTTP_403_FORBIDDEN)
        
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """Update a review instance."""
        review = self.get_object()
        if review.user != request.user:
            return Response({'error': 'You do not have permission to update this review.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing users."""
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to manage users

class SignupView(generics.CreateAPIView):
    """View for user registration."""
    
    serializer_class = UserSerializer  # Use the UserSerializer for signup

class ReviewByMovieView(generics.ListAPIView):
    """View to filter reviews by movie title."""
    
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = self.kwargs['title']
        return Review.objects.filter(movie_title__icontains=title)  # Corrected to filter by movie_title

class ReviewSearchView(generics.ListAPIView):
    """View to search reviews by title or rating."""
    
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        title = self.request.query_params.get('title', None)
        rating = self.request.query_params.get('rating', None)
        
        if title:
            queryset = queryset.filter(movie_title__icontains=title)  # Corrected to filter by movie_title
        
        if rating:
            queryset = queryset.filter(rating=rating)

        return queryset

def home(request):
    """Home view that returns a welcome message."""
    return HttpResponse("Welcome to the Movie Review API!")

class CustomAuthToken(ObtainAuthToken):
    """Custom Auth Token view."""
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=400)
