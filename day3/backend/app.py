from flask import Flask
from flask_security import Security, auth_required, roles_accepted
from flask_restful import Api

from models import db, user_datastore
from config import Config

def create_app():
    init_app = Flask(__name__)
    init_app.config.from_object(Config)

    db.init_app(init_app)
    Security(init_app, user_datastore)

    init_api = Api(init_app)
    return init_app, init_api

app, api = create_app()

from routes.auth import register, login
api.add_resource(register, '/auth/register')
api.add_resource(login, '/auth/login')

from routes.test import greet, add_contact, manage_contact
api.add_resource(greet, '/greet/<name>')
api.add_resource(add_contact, '/contact')
api.add_resource(manage_contact, '/contact/<int:id>')


@app.route('/hello', methods=['GET'])
@auth_required('token')
@roles_accepted('admin', 'user')
def hello():
    return "Hello, World!"

@app.route('/helloWorld')
@auth_required('token')
@roles_accepted('admin')
def hello_world():
    return {"message": "Hello, World!"}

if __name__ == '__main__':
    app.run()