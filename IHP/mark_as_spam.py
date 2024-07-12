import requests

# Define the base URL of your Django API
BASE_URL = 'http://localhost:8000/'

def mark_as_spam(phone_number, access_token):
    # Define the endpoint for marking a number as spam
    endpoint = BASE_URL + 'api/mark_as_spam/'

    # Define the headers with the access token
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    # Define the data to be sent in the request body
    data = {
        'phone_number': phone_number
    }

    try:
        # Make a POST request to mark the number as spam
        response = requests.post(endpoint, json=data, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Number marked as spam successfully!")
        else:
            print("Failed to mark number as spam. Status code:", response.status_code)
            print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # Example usage:
    access_token = '<Access Token>'
    phone_number = '<Phone number>'  # Replace with the phone number you want to mark as spam
    mark_as_spam(phone_number, access_token)
