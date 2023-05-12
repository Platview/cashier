from cash import db, bcrypt, login_manager
from sqlalchemy.sql import func
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Worker.query.get(int(user_id))

class Worker(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    employee_number = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(5000), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=5), unique=True)
    description = db.Column(db.String(150), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.name}'


class Calculator(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    Item_name = db.Column(db.String(150))
    item_price = db.Column(db.Integer(), nullable=False)
    item_quantity = db.Column(db.Integer(), nullable=False)
    item_total = db.Column(db.Integer(), nullable=False)


class Attendance(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    employee_number = db.Column(db.String(50), nullable=False)
    time_in = db.Column(db.DateTime(timezone=True), default=func.now())


class Left(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    worker = db.Column(db.String(50), nullable=False)
    time_out = db.Column(db.DateTime(timezone=True), default=func.now())

class Transactions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    worker = db.Column(db.String(50), nullable=False)
    transactions_all = db.Column(db.String(50))
    transactions_total = db.Column(db.Integer())