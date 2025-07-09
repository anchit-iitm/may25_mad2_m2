from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin
from datetime import datetime

db=SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number
        }
    
    def get_all():
        contacts = Contact.query.all()
        if contacts:
            list_of_contacts = []
            for contact in contacts:
                list_of_contacts.append(contact.serialize())
            return list_of_contacts
        else:
            return "No contacts found"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False) #
    password = db.Column(db.String(200), nullable=False) #

    login_count = db.Column(db.Integer) 
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))

    active = db.Column(db.Boolean) #
    fs_uniquifier = db.Column(db.String(255), unique=True) #
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False) #
    description = db.Column(db.String(255))

class roles_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    status = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(255), db.ForeignKey('user.id'))
    updated_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    delete = db.Column(db.Boolean, default=False)
    
    products = db.relationship('Product', back_populates='category', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'delete': self.delete,
            'products': [product.serialize() for product in self.products] if self.products else 'No products found'
        }
    
    def get_all():
        categories = Category.query.all()
        if not categories:
            return "No category found"
        return [category.serialize() for category in categories]

    def admin_delete(id):
        category = Category.query.filter_by(id=id).first()
        if not category:
            return "No category found by that id", False
        # delete category row with sql
        db.session.delete(category)
        db.session.commit()
        return "Category deleted successfully", True



class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    status = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(255), db.ForeignKey('user.id'))
    updated_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    delete = db.Column(db.Boolean, default=False)
    category = db.relationship('Category', back_populates='products', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'status': self.status,
            'category_id': self.category_id,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'delete': self.delete
        }
    
    def admin_delete(id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            return "No product found by that id", False
        # delete product row with sql
        db.session.delete(product)
        db.session.commit()
        return "Product deleted successfully", True