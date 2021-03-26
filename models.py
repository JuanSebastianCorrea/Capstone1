"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)

    favorites = db.relationship('Recipe', secondary='saved_recipes', backref='users')


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    @classmethod
    def signup(cls, username, password, email):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """
        Find user with `username` and `password`.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Recipe(db.Model):
    """Recipes"""

    __tablename__ = 'recipes'

    uri = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, nullable=False)
    cuisine_type = db.Column(db.Text, nullable=True)

    # ingredients nullable true for now
    ingredients = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)

    # user-made recipes may not have a url
    url = db.Column(db.Text, nullable=True)
    
    # recipes from Edamame are not associated with a particular user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)

    own_recipe = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'uri': self.uri,
            'name': self.name,
            'image_url': self.image_url,
            'cuisine_type': self.cuisine_type,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'url': self.url,
            'user_id': self.user_id,
            'own_recipe': self.own_recipe
        }

    def __repr__(self):
        return f"<Recipe {self.name}, {self.cuisine_type}, {self.user_id}>"


class FavoriteRecipe(db.Model):
    """Users' favorite recipes"""

    __tablename__ = 'saved_recipes'

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    recipe_uri = db.Column(db.Text, db.ForeignKey('recipes.uri', ondelete='cascade'), primary_key=True)


# class OwnRecipe(db.Model):
#     """User's own recipes"""

#     __tablename__ = 'own_recipes'

#     uri = db.Column(db.Text, primary_key=True)
#     name = db.Column(db.Text, nullable=False, unique=True)
#     image_url = db.Column(db.Text, nullable=False, unique=True)
#     cuisine_type = db.Column(db.Text, nullable=False, unique=True)
#     ingredients = db.Column(db.Text, nullable=False)
#     instructions = db.Column(db.Text, nullable=True)
    

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    # recipe_uri = db.Column(db.Text, db.ForeignKey('recipes_uri', ondelete='cascade'), unique=True)

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
