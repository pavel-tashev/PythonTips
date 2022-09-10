import os
from dotenv import load_dotenv
from flask import Flask, jsonify

from appExample import appExample
from auth.appAuth import appAuth, jwt

# SQLAlchemy
from auth.models.sqlaModels import db, bcrypt
# END SQLAlchemy

# MongoDb
# from auth.models.mongodbModels import bcrypt
# END MongoDb


load_dotenv()


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["JWT_COOKIE_SECURE"] = os.environ.get('COOKIE_SECURE')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(os.environ.get('ACCESS_TOKEN_LIFETIME'))
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = int(os.environ.get('ACCESS_TOKEN_LIFETIME'))

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
# END SQLAlchemy

app.register_blueprint(appAuth)
app.register_blueprint(appExample)

# SQLAlchemy
db.init_app(app)
# END SQLAlchemy

jwt.init_app(app)
bcrypt.init_app(app)



@app.errorhandler(404)
@app.errorhandler(405)
def uri_not_found(e) -> tuple:
    return jsonify([]), 404

if __name__ == "__main__":
    app.run(
        host = '0.0.0.0',
        port = os.getenv('PORT'),
        debug = bool(os.getenv('DEBUG'))
    )