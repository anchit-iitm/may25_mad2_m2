from flask import Flask, request
from flask_security import Security

from models import db, Contact, user_datastore
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
Security(app, user_datastore)



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {"message": "Please provide userrname, email, and password"}, 400

    if user_datastore.find_user(email=email):
        return {"message": "User already exists"}, 409
    
    if user_datastore.find_user(username=username):
        return {"message": "Username already exists"}, 409

    user = user_datastore.create_user(username=username, email=email, password=password)
    user_datastore.add_role_to_user(user, user_datastore.find_role('user'))
    db.session.commit()
    return {"message": "User registered successfully", "email": user.email, "id": user.id}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    if not email:
        return {"message": "Please provide an email"}, 400
    password = data.get('password')
    if not password:
        return {"message": "Please provide a password"}, 400
    
    user = user_datastore.find_user(email=email)
    if not user:
        return {"message": "User not found"}, 404
    
    if not user.password == password:
        return {"message": "Invalid password"}, 401
    
    if not user.active:
        return {"message": "User is inactive"}, 403
    
    from flask_security import login_user
    login_user(user)
    db.session.commit()
    print(user.roles)

    return {
        "message": "Login successful", 
        "email": user.email, "id": user.id, 
        "authToken": user.get_auth_token(), 
        "role": user.roles[0].name
        }, 200

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/helloWorld')
def hello_world():
    return {"message": "Hello, World!"}

@app.route('/greet/<name>')
def greet(name):
    return {"message":f"Hello, {name}!"}

@app.route('/contact', methods=['POST', 'GET'])
def add_contact():
    if request.method == "GET":
        contacts = Contact.query.all()
        if contacts:
            list_of_contacts = []
            for contact in contacts:
                json_for_this_row = {"Name": contact.name, "Number": contact.number}
                list_of_contacts.append(json_for_this_row)
            return {"data": list_of_contacts, "message": "Contacts retrieved successfully"}, 200
        else:
            return {"message": "No contacts found"}, 404
        
    if request.method == "POST":
        data = request.json
        name = data.get('name')
        number = data.get('number')
        if not name or not number:
            return {"message":"Please provide both name and number"}, 400
        try:
            contact = Contact(name=name, number=number)
            db.session.add(contact)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500
        return {"message": "Contact added successfully"}, 201

@app.route('/contact/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return {"message": "Contact not found"}, 404

    if request.method == "GET":
        return {"Name": contact.name, "Number": contact.number}, 200

    if request.method == "PUT":
        data = request.json
        name = data.get('name', contact.name)
        number = data.get('number', contact.number)
        if not name or not number:
            return {"message": "Please provide both name and number"}, 406
        contact.name = name
        contact.number = number
        db.session.commit()
        return {"message": "Contact updated successfully"}, 201

    if request.method == "DELETE":
        db.session.delete(contact)
        db.session.commit()
        return {"message": "Contact deleted successfully"}, 201

if __name__ == '__main__':
    app.run()