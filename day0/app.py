from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    contact = Contact.query.first()
    if not contact:
        return "noo contacts"
    return render_template('contact.html', phno=contact.number, name=contact.name)

@app.route('/addContact', methods=['GET', 'POST'])
def add_contact():
    if request.method == "GET":
        return render_template('add_contact.html')
    if request.method == "POST":
        data = request.form
        name = data.get('name')
        number = data.get('number')
        if not name or not number:
            return "Please provide both name and number", 400
        contact = Contact(name=name, number=number)
        db.session.add(contact)
        db.session.commit()
        return "Contact added successfully", 201

if __name__ == "__main__":
    app.run()