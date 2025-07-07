from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_required, roles_accepted

from models import db, Contact


# @app.route('/greet/<name>')
# @auth_required('token')
# @roles_accepted('admin', 'user')
# def greet(name):
class greet(Resource):
    @auth_required('token')
    @roles_accepted('admin', 'user')
    def get(self, name):
        return make_response(jsonify({"message":f"Hello, {name}!"}), 200)

# @app.route('/contact', methods=['POST', 'GET'])
# @auth_required('token')
# @roles_accepted('admin')
# def add_contact():
class add_contact(Resource):
    @auth_required('token')
    @roles_accepted('admin')
    def get(self):
        contacts = Contact.query.all()
        if contacts:
            list_of_contacts = []
            for contact in contacts:
                json_for_this_row = {"Name": contact.name, "Number": contact.number}
                list_of_contacts.append(json_for_this_row)
            return make_response(jsonify({"data": list_of_contacts, "message": "Contacts retrieved successfully"}), 200)
        else:
            return make_response(jsonify({"message": "No contacts found"}), 404)
        
    @auth_required('token')
    @roles_accepted('admin')
    def post(self):
        data = request.json
        name = data.get('name')
        number = data.get('number')
        if not name or not number:
            return make_response(jsonify({"message":"Please provide both name and number"}), 400)
        try:
            contact = Contact(name=name, number=number)
            db.session.add(contact)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": f"An error occurred: {str(e)}"}), 500)
        return make_response(jsonify({"message": "Contact added successfully"}), 201)

# @app.route('/contact/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @auth_required('token')
# @roles_accepted('admin')
# def manage_contact(id):
class manage_contact(Resource):

    @auth_required('token')
    @roles_accepted('admin')
    def get(self, id):
        contact = Contact.query.get(id)
        if not contact:
            return make_response(jsonify({"message": "Contact not found"}), 404)
        return make_response(jsonify({"Name": contact.name, "Number": contact.number}), 200)

    @auth_required('token')
    @roles_accepted('admin')
    def put(self, id):
        contact = Contact.query.get(id)
        if not contact:
            return make_response(jsonify({"message": "Contact not found"}), 404)
        data = request.json
        name = data.get('name', contact.name)
        number = data.get('number', contact.number)
        if not name or not number:
            return make_response(jsonify({"message": "Please provide both name and number"}), 406)
        contact.name = name
        contact.number = number
        db.session.commit()
        return make_response(jsonify({"message": "Contact updated successfully"}), 201)

    @auth_required('token')
    @roles_accepted('admin')
    def delete(self, id):
        contact = Contact.query.get(id)
        if not contact:
            return make_response(jsonify({"message": "Contact not found"}), 404)
        db.session.delete(contact)
        db.session.commit()
        return make_response(jsonify({"message": "Contact deleted successfully"}), 201)
