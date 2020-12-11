import base64
import requests
import datetime

client_id = 'd4dba07180974c278572a290fdda637f'
client_secret = '16d045de6a834496a2b5a812ea156ced'

class SpotifyAPI(object):
    token_url = 'https://accounts.spotify.com/api/token'
    access_token = None
    access_token_did_expire = True
    access_token_expires = datetime.datetime.now()
    client_id = None
    client_secret = None

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception('You must set client_id and client_secret')
        client_creds = f'{client_id}:{client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            'Authorization': f'Basic {client_creds_b64}'
            }

    def get_token_data(self):
        return {
            'grant_type': 'client_credentials'
            }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url,data = token_data,headers = token_headers)
        print(r.json())
        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        acccess_token = data['access_token']
        expires_in = data['expires_in']
        self.access_token_expires = now + datetime.timedelta(seconds=expires_in)
        self.acccess_token_did_expire = self.access_token_expires < now
        return True
        
client = SpotifyAPI(client_id, client_secret)
print (client.perform_auth())