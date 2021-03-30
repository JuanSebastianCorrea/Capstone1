"""Recipe Modelt Tests"""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Recipe

os.environ['DATABASE_URL'] = "postgresql:///recipes_db_test"

from app import app



class MessageModelTestCase(TestCase):
    """Test message model"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 33333
        u = User.signup("testing", "password", "testing@test.com")
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
        
    def test_recipe_model(self):
        """Does the basic model work?"""
        recipe = Recipe(uri="testuri", name="testname", image_url="test_image_url")

        db.session.add(recipe)
        db.session.commit()

        recipes = Recipe.query.all()

        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].uri, "testuri")
        self.assertEqual(recipes[0].name, "testname")
        self.assertEqual(recipes[0].image_url, "test_image_url")


    # Is this test even useful?
    def test_user_own_recipes(self):
        """Are recipes made by a user?"""

        recipe1 = Recipe(uri="testuri", name="testname", image_url="test_image_url", user_id=self.uid)
        recipe2 = Recipe(uri="testuri2", name="testname2", image_url="test_image_url2")

        db.session.add_all([recipe1, recipe2])
        db.session.commit()

        self.assertEqual(recipe1.user_id, self.uid)
        self.assertNotEqual(recipe2.user_id, self.uid)
        self.assertEqual(recipe2.user_id, None)


