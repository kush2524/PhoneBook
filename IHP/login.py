import requests

# Define the base URL of your Django API
BASE_URL = 'http://localhost:8000/api/'

def login(username, password):
    # Define the endpoint for user login
    endpoint = BASE_URL + 'login/'

    # Define the data to be sent in the request body
    data = {
        'username': username,
        'password': password
    }

    try:
        # Make a POST request to login
        response = requests.post(endpoint, data=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the access token received in the response
            print("Login successful! Access token:", response.json()['access'])
        else:
            print("Failed to login. Status code:", response.status_code)
            print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    #Add your credentials to get you JWT Token
    login('<Username>', '<Password>')
