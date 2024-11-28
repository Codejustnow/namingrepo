import requests
import json

# Your Azure AD tenant and app registration details
tenant_id = "your-tenant-id"
client_id = "your-client-id"
client_secret = "your-client-secret"
authority = "https://login.microsoftonline.com/" + tenant_id

# Step 1: Get access token using client credentials flow
def get_access_token():
    url = f"{authority}/oauth2/v2.0/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        print(f"Error getting access token: {response.text}")
        return None

# Step 2: Call Microsoft Graph API to get sign-in logs
def get_failed_signins(access_token):
    url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
    
    # Filter to fetch only failed sign-ins
    params = {
        "$filter": "status/errorCode ne 0",  # This will filter for failed sign-ins
        "$top": 10  # Limit to the top 10 entries for simplicity
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for sign_in in data["value"]:
            print(json.dumps(sign_in, indent=4))
    else:
        print(f"Error fetching sign-ins: {response.text}")

# Step 3: Run the functions
access_token = get_access_token()
if access_token:
    get_failed_signins(access_token)
