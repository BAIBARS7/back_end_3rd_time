from rest_framework import serializers
from .models import Review, CustomUser  # Import CustomUser model
from django.core.exceptions import ValidationError as DjangoValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model."""
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """Ensure the email is unique."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        """Create a new user instance."""
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update an existing user instance."""
        instance.username = validated_data.get('username', instance.username)

        # Validate and update email only if it's being changed
        email = validated_data.get('email', None)
        if email and email != instance.email:
            if CustomUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("This email is already in use.")
            instance.email = email
        
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)  # Hash the new password
        
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """Ensure the email is unique."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        """Create a new user instance."""
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),  # Provide a queryset for the user field
        required=False,
        allow_null=True  # Make user optional
    )

    class Meta:
        model = Review
        fields = '__all__'  # Alternatively, you can specify fields explicitly if needed.

    def validate_rating(self, value):
        """Ensure the rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        """Create a new review instance."""
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing review instance."""
        instance.movie_title = validated_data.get('movie_title', instance.movie_title)
        instance.content = validated_data.get('content', instance.content)
        instance.rating = validated_data.get('rating', instance.rating)
        
        # Ensure that only the owner can update their review (if needed)
        if 'user' in validated_data:
            instance.user = validated_data['user']
        
        instance.save()
        return instance
