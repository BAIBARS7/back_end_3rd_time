from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Review

class ReviewAPITest(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')  # Log in the user

    def test_create_review(self):
        """Test creating a review."""
        url = reverse('reviews-list')  # Adjust to your actual URL name
        data = {
            'movie_title': 'Test Movie',
            'content': 'This is a test review.',
            'rating': 5,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)  # Verify that one review has been created
        self.assertEqual(Review.objects.get().movie_title, 'Test Movie')  # Verify the movie title

    def test_get_reviews(self):
        """Test retrieving reviews."""
        url = reverse('reviews-list')  # Adjust to your actual URL name
        Review.objects.create(movie_title='Test Movie', content='This is a test review.', rating=5, user=self.user)  # Create a review for testing
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure we get one review back

    def test_update_review(self):
        """Test updating a review."""
        review = Review.objects.create(movie_title='Test Movie', content='Initial content', rating=3, user=self.user)
        url = reverse('reviews-detail', args=[review.id])  # Adjust to your actual URL name
        data = {'content': 'Updated content'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()  # Refresh the review instance from the database
        self.assertEqual(review.content, 'Updated content')  # Verify the content was updated

    def test_delete_review(self):
        """Test deleting a review."""
        review = Review.objects.create(movie_title='Test Movie', content='To be deleted', rating=2, user=self.user)
        url = reverse('reviews-detail', args=[review.id])  # Adjust to your actual URL name
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)  # Verify that no reviews remain

    def test_create_review_unauthenticated(self):
        """Test creating a review without authentication."""
        self.client.logout()  # Log out the user
        url = reverse('reviews-list')  # Adjust to your actual URL name
        data = {
            'movie_title': 'Another Test Movie',
            'content': 'This should fail.',
            'rating': 4,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expect forbidden status
