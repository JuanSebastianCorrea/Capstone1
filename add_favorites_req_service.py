import requests

API_ID = '7ad5f5c3'
API_KEY = '75d853b05cbe14a1b05b4fd0c1f472bc'
BASE_URL = 'https://api.edamam.com/search?'

def get_recipe(recipe_uri):
    resp = requests.get(f'{BASE_URL}', params= {'r' : recipe_uri, 'app_id' : API_ID, 'app_key' : API_KEY})
    return resp.json()

