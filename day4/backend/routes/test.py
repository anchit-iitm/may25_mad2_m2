from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_required, roles_accepted

from models import db, Contact

class greet(Resource):
    @auth_required('token')
    @roles_accepted('admin', 'user')
    def get(self, name):
        return make_response(jsonify({"message":f"Hello, {name}!"}), 200)
    
class add_contact(Resource):
    @auth_required('token')
    @roles_accepted('admin')
    def get(self):
        # contacts = Contact.query.all()
        # if contacts:
            # list_of_contacts = []
            # for contact in contacts:
            #     list_of_contacts.append(contact.serialize())
        data = Contact.get_all()
        if data != "No contacts found":
            return make_response(jsonify({"data": data, "message": "Contacts retrieved successfully"}), 200)
        else:
            return make_response(jsonify({"message": data}), 404)
        
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
