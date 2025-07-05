from flask import request, jsonify, make_response
from flask_restful import Resource

from models import db, user_datastore

# @app.route('/auth/register', methods=['POST'])
# def register():
class register(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return make_response(jsonify({"message": "Please provide userrname, email, and password"}), 400)

        if user_datastore.find_user(email=email):
            return make_response(jsonify({"message": "User already exists"}), 409)
        
        if user_datastore.find_user(username=username):
            return make_response(jsonify({"message": "Username already exists"}), 409)

        user = user_datastore.create_user(username=username, email=email, password=password)
        user_datastore.add_role_to_user(user, user_datastore.find_role('user'))
        db.session.commit()
        return make_response(jsonify({"message": "User registered successfully", "email": user.email, "id": user.id}), 201)

class login(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        if not email:
            return make_response(jsonify({"message": "Please provide an email"}), 400)
        password = data.get('password')
        if not password:
            return make_response(jsonify({"message": "Please provide a password"}), 400)
        
        user = user_datastore.find_user(email=email)
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        if not user.password == password:
            return make_response(jsonify({"message": "Invalid password"}), 401)
        
        if not user.active:
            return make_response(jsonify({"message": "User is inactive"}), 403)
        
        from flask_security import login_user
        login_user(user)
        db.session.commit()

        return make_response(jsonify({
            "message": "Login successful", 
            "email": user.email, "id": user.id, 
            "authToken": user.get_auth_token(), 
            "role": user.roles[0].name
            }), 200)
