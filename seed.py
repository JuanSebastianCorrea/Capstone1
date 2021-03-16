from app import app
from models import db, User, FavoriteRecipe, Recipe


db.drop_all()
db.create_all()

u1 = User(
    username="Ruru",
    password="$2b$12$ix4rOP/HWQnWzuwpMnio.OQfVyuZmeO7rO5ADBwMo4t.tB8puRpVC",
    email="lulu@gmail.com"
)




db.session.add(u1)
db.session.commit()