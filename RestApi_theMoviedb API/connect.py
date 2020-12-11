import requests
import pprint
import pandas as pd

api_key = 'cd32abc2a27c6feb4a3f2e938b3d07b3'
api_key_v4 = ''
# https://api.themoviedb.org/3/movie/550?api_key=cd32abc2a27c6feb4a3f2e938b3d07b3


movie_id = 500
api_version = 3
api_base_url = f'https://api.themoviedb.org/{api_version}'
endpoint_path = f'/movie/{movie_id}'
endpoint = f'{api_base_url}{endpoint_path}?api_key={api_key}'

# r = requests.get(endpoint)
# print(type(endpoint))
# print(r.status_code)
# print(r.text)

# output = 'movies.csv'
api_version = 3
search_query = 'The Matrix'
api_base_url = f'https://api.themoviedb.org/{api_version}'
endpoint_path = f'/search/movie'
endpoint = f'{api_base_url}{endpoint_path}?api_key={api_key}&query={search_query}'
r = requests.get(endpoint)
# pprint.pprint(r.json())


# print(s['results'][1]['id'])

# print(s.keys())

if r.status_code == 200:
    s = r.json()
    results = s['results']
    if len(s) != 0:
        movies= {}
        for result in results:
            id = result['id']
            title = result['original_title']
            movie = {id: title}  
            movies.update(movie)
        pprint.pprint(movies)
        # df = pd.DataFrame(movies)    
        # print(df.head())
        # df.to_csv(output, index=False)