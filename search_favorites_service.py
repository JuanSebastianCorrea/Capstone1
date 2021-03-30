from models import User, Recipe

def search_favorites(user_id, searchterm):
    curr_user = User.query.get_or_404(user_id)
    favorites = curr_user.favorites

    if searchterm == 'all':
        serialized_favs = [f.serialize() for f in favorites]
                        
        return serialized_favs

    favorites_uri = [r.uri for r in favorites]
  
    serialized_favs = [f.serialize() for f in Recipe.query.filter((Recipe.uri.in_(favorites_uri)) & (Recipe.name.ilike(f"%{searchterm}%"))).all()]
                        
    return serialized_favs