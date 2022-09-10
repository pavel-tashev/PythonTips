import os
from dotenv import load_dotenv
from flask import Flask, jsonify

from appExample import appExample
from auth.appAuth import session, login_manager, appAuth

# SQLAlchemy
from auth.models.sqlaModels import db, bcrypt
# END SQLAlchemy

# MongoDb
# from auth.models.mongodbModels import client, bcrypt
# END MongoDb


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = int(os.environ.get('SESSION_LIFETIME'))

# SQLAlchemy
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
# END SQLAlchemy

# MongoDb
# app.config['SESSION_TYPE'] = 'mongodb'
# app.config['SESSION_MONGODB'] = client
# app.config['SESSION_MONGODB_DB'] = os.environ.get('MONGODB_NAME')
# app.config['SESSION_MONGODB_COLLECT'] = os.environ.get('SESSIONS_TABLE')
# END MongoDb

app.register_blueprint(appAuth)
app.register_blueprint(appExample)

# SQLAlchemy
db.init_app(app)
# END SQLAlchemy

bcrypt.init_app(app)
session.init_app(app)
login_manager.init_app(app)



@app.errorhandler(404)
@app.errorhandler(405)
def uri_not_found(e) -> tuple:
    return jsonify([]), 404

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = os.getenv('PORT'),
        debug = bool(os.getenv('DEBUG'))
    )