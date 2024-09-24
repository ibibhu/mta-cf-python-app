import os
import json
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)


@app.route('/destinations')
def list_destinations():
    try:
        token = get_access_token()
        destinations = get_destination_details(token)
        return jsonify(destinations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve data from the OData service via Destination service
@app.route('/odata')
def get_odata_data():
    try:
        # Step 1: Get access token from Destination service
        token = get_access_token()
        
        # Step 2: Fetch destination details from the binding
        destination = get_destination_details(token)
        
        # Step 3: Call OData service via destination
        odata_response = call_odata_service(destination, token)
        
        return jsonify(odata_response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_access_token():
    """Fetch OAuth token from the Destination service using credentials from VCAP_SERVICES."""
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    token_url = os.getenv('TOKEN_URL') + "/oauth/token"  # Append /oauth/token for the token endpoint

    # OAuth token request
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(token_url, data=data, headers=headers)
    response.raise_for_status()
    return response.json().get('access_token')

def get_destination_details(token):
    """Fetch destination details from the binding."""
    # Get the VCAP_SERVICES environment variable
    vcap_services = os.getenv('VCAP_SERVICES')
    
    if not vcap_services:
        raise Exception("VCAP_SERVICES environment variable is not set")
    
    # Parse the JSON binding to retrieve Destination service details
    services = json.loads(vcap_services)
    
    # Access the destination service configuration
    destination_service = services.get('destination')
    
    if not destination_service:
        raise Exception("No destination service found in VCAP_SERVICES")
    
    # Assuming we want the first destination service instance
    destination_instance = destination_service[0]['credentials']
    
    uri = destination_instance.get('uri')
    
    # Call the Destination service REST API to fetch destinations
    destinations = call_destination_service_api(uri, token)
    
    if not destinations:
        raise Exception("No destinations found")
    
    return destinations[0]  # Returning the first destination for simplicity

def call_destination_service_api(uri, token):
    """Call the Destination service REST API to get the list of destinations."""
    response = requests.get(f"{uri}/destination-configuration/v1/subaccountDestinations", 
                            headers={'Authorization': f'Bearer {token}'})
    response.raise_for_status()
    return response.json()

def call_odata_service(destination, token):
    """Call the OData service via the destination."""
    odata_url = destination.get('URL') +  "?$skip=0&$top=1&$format=json"
    auth_type = destination.get('Authentication')
    
    headers = {'Authorization': f'Bearer {token}'}  # For Bearer token based authentication

    if auth_type == "BasicAuthentication":
        username = destination.get('User')
        password = destination.get('Password')
        response = requests.get(odata_url, auth=(username, password), headers=headers)
    else:
        response = requests.get(odata_url, headers=headers)
    
    response.raise_for_status()
    return response.json()

@app.route('/')
def home():
    return jsonify({"message": "Hello from Cloud Foundry!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
