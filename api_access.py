import requests
import time

# Substitua as informações abaixo pelas informações fornecidas
username = ""
password = ""
api_key = ""
client_id = ""
client_secret = ""

auth_url = "https://app.ynnovbooking.com/oauth/token"
api_base_url = "https://app.ynnovbooking.com/api/web/v2"

# Autenticar e recuperar o access_token e o tempo de expiração
def authenticate(username, password, client_id, client_secret):
    auth_data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(auth_url, data=auth_data)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Authentication failed, check your credentials")

# Renovar o access_token
def renew_token(refresh_token, client_id, client_secret):
    auth_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(auth_url, data=auth_data)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Failed to renew access token")

# Acessar a API usando o Bearer token e a api_key
def access_api(token, api_key, endpoint):
    headers = {
        "Authorization": f"Bearer {token}",
        "api_key": api_key,
        "Content-Type": "application/json",
    }
    response = requests.get(f"{api_base_url}/{endpoint}", headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        return None
    else:
        raise ValueError(f"Failed to access API, status code: {response.status_code}")

if __name__ == "__main__":
    auth_data = authenticate(username, password, client_id, client_secret)
    access_token = auth_data["access_token"]
    refresh_token = auth_data["refresh_token"]
    expires_in = auth_data["expires_in"]
    print("Authentication successful, access token retrieved.")
    print(f"Token expires in {expires_in} seconds.")

    # Substitua 'your_endpoint' pelo endpoint da API desejado
    endpoint = "availability"

    # Acessar a API e lidar com a expiração do token
    api_data = access_api(access_token, api_key, endpoint)
    if api_data is not None:
        print("API data:", api_data)
    else:
        print("Token expired, renewing token...")
        auth_data = renew_token(refresh_token, client_id, client_secret)
        access_token = auth_data["access_token"]
        expires_in = auth_data["expires_in"]
        print("New token retrieved, expires in", expires_in, "seconds.")
        api_data = access_api(access_token, api_key, endpoint)
        print("API data:", api_data)
