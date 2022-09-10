from app import app
from auth.models.sqlaModels import db

with app.app_context():
    db.create_all()