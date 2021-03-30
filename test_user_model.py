"""User model tests."""

# to run these tests:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Recipe, FavoriteRecipe

os.environ['DATABASE_URL'] = "postgresql:///recipes_db_test"



from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "password", "email1@email.com")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "password", "email2@email.com")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="testuser",
            password="HASHED_PASSWORD",
            email="test@test.com"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no favorites
        self.assertEqual(len(u.favorites), 0)


    ####
    #
    # Signup Tests
    #
    ####
    def test_valid_signup(self):
        """Does valid signup work?"""

        u_test = User.signup("testtesttest", "password", "testtest@test.com")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertNotEqual(u_test.password, "password")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        """Does invalid username raise error?"""

        invalid = User.signup(None, "password", "test@test.com")
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        """Does invalid email raise error?"""

        invalid = User.signup("testtest", "password", None)
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        """Does invalid password or empty password field raise error?"""

        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "", "email@email.com")
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", None, "email@email.com")
    
    ####
    #
    # Authentication Tests
    #
    ####
    def test_valid_authentication(self):
        """Does valid authentication work?"""

        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        """Does invalid username fail authentication"""

        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        """Does invalid password fail authentication"""

        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))




        
    ####
    #
    # Favorites tests
    #
    ####
    def test_user_favorites(self):
        """Does User "favorites" property show relationship between User and Recipe correctly?"""

        r = Recipe(uri="recipe_uri", name="recipe_name", image_url="recipe_image_url")
        db.session.add(r)
        db.session.commit()

        favRec = FavoriteRecipe(user_id=self.uid1, recipe_uri=r.uri)
        db.session.add(favRec)
        db.session.commit()

        self.assertEqual(len(self.u1.favorites), 1)
        self.assertEqual(len(self.u2.favorites), 0)

        self.assertEqual(self.u1.favorites[0].uri, "recipe_uri")
        self.assertEqual(self.u1.favorites[0].name, "recipe_name")
        self.assertEqual(self.u1.favorites[0].image_url, "recipe_image_url")
        

   



        

