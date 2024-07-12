import requests

# Define the base URL of your Django API
BASE_URL = 'http://localhost:8000/api/'

def search_phone_number(phone_number, access_token):
    # Define the endpoint for searching a phone number
    endpoint = BASE_URL + 'search_phone_number/'

    # Define the headers, including the Authorization token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Define the parameters to be sent in the query string
    params = {
        'phone_number': phone_number
    }

    try:
        # Make a GET request to search for the phone number
        response = requests.get(endpoint, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Search successful!")
            print("Response:", response.json())
        else:
            print("Failed to search phone number. Status code:", response.status_code)
            print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

# Example usage
if __name__ == "__main__":
    # Replace with the phone number you want to search and a valid access token
    phone_number = '<Number>'
    access_token = '<Access Token>'
    search_phone_number(phone_number, access_token)
