from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# App initialization
app = Flask(__name__)
# Path Configurations
basedir = os.path.abspath(os.path.dirname(__file__))

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# init Db ORM ( SQLAlchemy )
db = SQLAlchemy(app)

# init Serializer ( Marshmallow ) 
ma = Marshmallow(app)

# Class Model SQL
class User(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(100))
    last_name   = db.Column(db.String(100))
    is_active   = db.Column(db.Boolean)

    def __init__(self, first_name, last_name, is_active):
        self.first_name = first_name
        self.last_name  = last_name 
        self.is_active  = is_active

# Class Schema
class UserSchema(ma.Schema):
    class Meta:
        fields  = ('id', 'first_name', 'last_name', 'is_active')

# Init Schema
user_schema     = UserSchema()
users_schema    = UserSchema(many=True)


# Routes
# fetch all users       --> /users 
# fetch signle user     --> /user/<id>
# update user           --> /user/update/id
# create user           --> /user/create

@app.route('/user/create', methods=['POST'])
def create_user():
    first_name  = request.json['first_name']
    last_name   = request.json['last_name']
    is_active    = request.json['is_active']

    new_user = User(first_name, last_name, is_active)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/users', methods=['GET'])
def fetch_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@app.route('/user/<id>', methods=['GET'])
def fetch_user(id):
    user = User.query.get(id)
    return jsonify(user_schema.dump(user)) 


@app.route('/user/update', methods=['PUT'])
def update_user():
    user = User.query.get(id)
    first_name  = request.json['first_name']
    last_name   = request.json['last_name']
    is_active    = request.json['is_active']

    new_user = User(first_name, last_name, is_active)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# Run the server
if __name__ == '__main__':
    app.run(debug=True)



























    
