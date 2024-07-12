import requests

# Define the base URL of your Django API
BASE_URL = 'http://localhost:8000/api/'

def register_user(username, phone_number, email, password):
    # Define the endpoint for user registration
    endpoint = BASE_URL + 'register/'

    # Define the data to be sent in the request body
    data = {
        'username': username,
        'phone_number': phone_number,
        'email': email,
        'password': password
    }

    try:
        # Make a POST request to register a new user
        response = requests.post(endpoint, json=data)

        # Check if the request was successful (status code 201)
        if response.status_code == 201:
            print("User registered successfully!")
        else:
            print("Failed to register user. Status code:", response.status_code)
            print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # Enter the credentials you want to register through
    register_user('<name>', '<number>', '<Email>', '<password>')
