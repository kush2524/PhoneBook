import requests

# Define the base URL of your Django API
BASE_URL = 'http://localhost:8000/'

# Replace YOUR_ACCESS_TOKEN with the actual access token
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

def search_by_name(name):
    # Define the endpoint for searching by name
    endpoint = BASE_URL + 'api/search_by_name/'

    # Define the data to be sent in the request body
    data = {'name': name}

    # Define the headers with the access token
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

    try:
        # Make a GET request to search by name
        response = requests.get(endpoint, params=data, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            if data:
                print("Search results:")
                for entry in data:
                    if 'name' in entry:
                        name = entry['name']
                    else:
                        name = "Not Available"
                    phone_number = entry.get('phone_number', "Not Available")
                    spam_count = entry.get('spam', "Not Available")
                    print(f"Name: {name}, Phone Number: {phone_number}, Spam Count: {spam_count}")
            else:
                print("No results found.")
        else:
            print("Failed to search by name. Status code:", response.status_code)
            print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

# Write the name that needs to be searched
search_by_name('<name>')
