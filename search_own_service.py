from models import User, Recipe

def search_own(user_id, searchterm):

    curr_user = User.query.get_or_404(user_id)
    own_recipes = Recipe.query.filter(Recipe.user_id == curr_user.id).all()

    if searchterm == 'all':
        serialized_own = [o.serialize() for o in own_recipes]
                        
        return serialized_own
    
    own_recipes_uri = [o.uri for o in own_recipes]
    serialized_own = [o.serialize() for o in Recipe.query.filter((Recipe.uri.in_(own_recipes_uri)) & (Recipe.name.ilike(f"%{searchterm}%"))).all()]
    return serialized_own