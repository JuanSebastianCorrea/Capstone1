"""My Recipes Views tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_my_recipes_views.py


import os
from unittest import TestCase

from models import db, connect_db, Recipe, User

os.environ['DATABASE_URL'] = "postgresql:///recipes_db_test"


from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class MyRecipesViewsTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    password="testuser",
                                    email="test@test.com")

        self.testuser_id = 1111
        self.testuser.id = self.testuser_id

        db.session.commit()

        r = Recipe(uri="testuri", name="testname", image_url="test_image_url", ingredients="", instructions="", user_id=self.testuser.id, own_recipe=True)
        
        db.session.add(r)
        db.session.commit()

    def test_view_my_recipes(self):
        """Can logged-in user view own recipes"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            r = Recipe.query.get("testuri")

            resp = c.get(f'/my_recipes')
           
            self.assertEqual(resp.status_code, 200)
            self.assertIn(r.name, str(resp.data))

    def test_view_my_recipes_no_session_user(self):
        """Does anonimous user get intercepted and redirected to sing-in page when attempting to view my_recipes page?"""

        with self.client as c:
            resp = c.get("/my_recipes", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please log in first!", str(resp.data))


    def test_view_recipe(self):
        """Can logged-in user view own full recipe card?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            r = Recipe.query.get("testuri")

            resp = c.get(f'/my_recipes/{r.uri}')
        
            self.assertEqual(resp.status_code, 200)
            self.assertIn(r.name, str(resp.data))
            self.assertIn("Directions", str(resp.data))
            self.assertIn("Ingredients", str(resp.data))


    def test_delete_my_recipe(self):
        """Is recipe deleted from user's own recipes?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            r = Recipe.query.get("testuri")
               
            resp = c.post(f'/my_recipes/delete', data={"delete-my-recipe-input" : r.uri}, follow_redirects=True)
                
            self.assertEqual(resp.status_code, 200)
    

    # def test_add_recipe(self):
    #     """Does a new recipe get added?"""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         resp = c.post("/my_recipes/add_recipe", data={"uri" : "testuri2", "name" : "testname2", "image_url" : "test_image_url2", "ingredients" : "testingredients2", "instructions" : "testinstructions2", "user_id" : self.testuser.id, "own_recipe" : True})
            
    #         # Make sure it redirects
    #         self.assertEqual(resp.status_code, 302)

    #         # recipes = Recipe.query.all()
    #         recipe = Recipe.query.get("testuri2")
    #         import pdb
    #         pdb.set_trace()
    #         # self.assertEqual(len(recipes), 2)
    #         self.assertEqual(recipe.name, "testname2")
    #         self.assertEqual(recipe.image_url, "test_image_url2")
    #         self.assertEqual(recipe.ingredients, "testingredients2")
    #         self.assertEqual(recipe.instructions, "testinstructions2")
    #         self.assertEqual(recipe.user_id, 1111)
    #         self.assertEqual(recipe.own_recipe, True)


#    def test_edit_my_recipe(self):
#        """Does an existing recipe get updated when edited?"""

