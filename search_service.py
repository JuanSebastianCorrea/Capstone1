import requests
from models import User

API_ID = '7ad5f5c3'
API_KEY = '75d853b05cbe14a1b05b4fd0c1f472bc'
BASE_URL = 'https://api.edamam.com/search?'

def search(user_id, searchterm, frm, to):

    resp = requests.get(f"{BASE_URL}q={searchterm}&app_id={API_ID}&app_key={API_KEY}&from={frm}&to={to}")
    if not user_id:
        return resp.json()["hits"]



    curr_user = User.query.get_or_404(user_id)
    saved_recipes = curr_user.favorites
    saved_recipes_uris = [r.uri for r in saved_recipes]

    recipes_list = []
 
    for item in resp.json()["hits"]:
        # import pdb
        # pdb.set_trace()
        if item.get("recipe").get("uri") in saved_recipes_uris:
            item["bookmarked"] = True
        recipes_list.append(item)
        print(item.get("bookmarked"))

    return recipes_list