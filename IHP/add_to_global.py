import requests

# Define the base URL of your Django API
BASE_URL = 'http://localhost:8000/'

# Replace 'YOUR_ACCESS_TOKEN' with the actual access token
ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3NzkxOTE3LCJpYXQiOjE3MTc3OTE2MTcsImp0aSI6IjJjZTlkNTljMGUyYzQ1N2U4YmE0YTdlM2JjNWNlMTY0IiwidXNlcl9pZCI6Mn0.IHb6Bvp97nxOr_Xe2GR_8mHATu4o9tdM9flPidmL71U'
def add_to_global_dataset(phone_number, name):
    # Define the endpoint for adding to the global dataset
    endpoint = BASE_URL + 'api/add_to_global_dataset/'

    # Define the data to be sent in the request body
    data = {
        'phone_number': phone_number,
        'name': name
    }

    # Define the headers with the access token
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

    try:
        # Make a POST request to add an entry to the global dataset
        response = requests.post(endpoint, json=data, headers=headers)

        # Check if the request was successful (status code 201)
        if response.status_code == 201:
            print("Entry added successfully!")
        else:
            print("Failed to add entry. Status code:", response.status_code)
            print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

# Add the number and name that needs to be send to global dataset
add_to_global_dataset('<number>', '<name>')
