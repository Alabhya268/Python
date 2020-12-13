import base64
import requests
import datetime
import pprint
from urllib.parse import urlencode

# Have your application request authorization
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
            raise Exception('Could not authenticate client')
            # return False
        data = r.json()
        now = datetime.datetime.now()
        self.access_token = data['access_token']
        expires_in = data['expires_in']
        self.access_token_expires = now + datetime.timedelta(seconds=expires_in)
        self.acccess_token_did_expire = self.access_token_expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        return headers

    def get_resource(self, lookup_id, resource_type = 'album', version = 'v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers = headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(_id, resource_type = 'albums')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type = 'artists')

    def search(self, query, search_type = 'artist'):
        headers = self.get_resource_header()
        endpoint = 'https://api.spotify.com/v1/search'
        data = urlencode({
            'q': 'Time ',
            'type': search_type.lower()
        })
        look_url = f'{endpoint}?{data}'
        print(look_url)
        r = requests.get(look_url,headers = headers)
        pprint.pprint(r.json())
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

spotifyAPI = SpotifyAPI(client_id, client_secret)
spotifyAPI.search('Time', search_type='track')