import requests

# Define the URL for your API endpoint
url = 'http://127.0.0.1:8000/api/reviews/'  # Adjust based on your actual API endpoint

# Prepare the data for the new review
data = {
    'movie_title': 'Inception',
    'content': 'A mind-bending thriller that keeps you guessing.',
    'rating': 5,
}

# Optional: Add authentication headers if required (e.g., JWT token)
headers = {
    'Authorization': 'Bearer YOUR_JWT_TOKEN_HERE',  # Replace with your actual token
}

# Send POST request
response = requests.post(url, json=data, headers=headers)

# Print the response status code and content
print(f'Status Code: {response.status_code}')
print('Response JSON:', response.json())  # Assuming the response is in JSON format
