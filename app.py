from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ
import logging
from dotenv import load_dotenv

# environment variables from .env file
load_dotenv()

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

@app.route('/')
def index():
    return "Hello World!"

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'test successful'}), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    try:
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'user created'}), 201
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        return jsonify({'message': 'error creating user', 'error': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.json() for user in users]), 200
    except Exception as e:
        logging.error(f"Error getting users: {e}")
        return jsonify({'message': 'error getting users'}), 500

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return jsonify({'user': user.json()}), 200
        return jsonify({'message': 'user not found'}), 404
    except Exception as e:
        logging.error(f"Error getting user: {e}")
        return jsonify({'message': 'error getting user'}), 500

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        try:
            db.session.commit()
            return jsonify({'message': 'user updated'}), 200
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            return jsonify({'message': 'error updating user'}), 500
    return jsonify({'message': 'user not found'}), 404

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'user deleted'}), 200
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            return jsonify({'message': 'error deleting user'}), 500
    return jsonify({'message': 'user not found'}), 404

if __name__ == '__main__':
    app.run(debug=environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'])