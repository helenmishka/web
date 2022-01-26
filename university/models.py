from flask_login import UserMixin
from flask import jsonify
from university import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    sign_login = db.Column(db.String(100), primary_key=True, nullable=True, unique=True)
    sign_password = db.Column(db.String(100), nullable=True)
    sign_role = db.Column(db.Integer, nullable=True)

    def get_id(self):
        return (self.sign_login)


class Customers(db.Model):
    __tablename__ = 'customers'
    namecustomer = db.Column(db.String(256), nullable=True)
    birthdaycustomer = db.Column(db.Date, nullable=True)
    passportdetails = db.Column(db.Integer, nullable=True, primary_key=True)
    login = db.Column(db.String(256), db.ForeignKey('users.sign_login'), nullable=True)

    def __repr__(self):
        return '{namecustomer: %r,  birthdaycustomer: %r, passportdetails: %r, login: %r}' % (
            self.namecustomer, self.birthdaycustomer, self.passportdetails, self.login)


class Workers(db.Model):
    __tablename__ = 'workers'
    idworker = db.Column(db.Integer, primary_key=True, nullable=True)
    nameworker = db.Column(db.String(256), nullable=True)
    postworker = db.Column(db.String(256), nullable=True)
    phonenumber = db.Column(db.String(256), nullable=True)
    login = db.Column(db.String(256), db.ForeignKey('users.sign_login'), nullable=True)

    def __repr__(self):
        return '{idworker: %r,  nameworker: %r, postworker: %r, phonenumber: %r, login: %r}' % (
            self.idworker, self.nameworker, self.postworker, self.phonenumber, self.login)


class Executors(db.Model):
    __tablename__ = 'executors'
    faculty = db.Column(db.String(256), nullable=True)
    department = db.Column(db.Integer, nullable=True)
    idexecutor = db.Column(db.Integer, nullable=True, primary_key=True)

    def __repr__(self):
        return '{faculty: %r,  department: %r, idexecutor: %r}' % (
            self.faculty, self.department, self.idexecutor)


class Directions(db.Model):
    __tablename__ = 'directions'
    typedirection = db.Column(db.String(256), nullable=True)
    iddirection = db.Column(db.String(256), primary_key=True, nullable=True)
    namedirection = db.Column(db.String(256), nullable=True)
    idexecutor = db.Column(db.Integer, db.ForeignKey('executors.idexecutor'), nullable=True)

    def __repr__(self):
        return '{typedirection: %r,  iddirection: %r, namedirection: %r, idexecutor: %r}' % (
            self.typedirection, self.iddirection, self.namedirection, self.idexecutor)


class Contracts(db.Model):
    __tablename__ = 'contracts'
    numbercontract = db.Column(db.Integer, primary_key=True, nullable=True)
    datecontract = db.Column(db.Date, nullable=True)
    typecontract = db.Column(db.String(256), nullable=True)
    periodcontract = db.Column(db.String(256), nullable=True)
    statuscontract = db.Column(db.String(256), nullable=True)
    valuecontract = db.Column(db.Integer, nullable=True)
    customerpassport = db.Column(db.Integer, db.ForeignKey('customers.passportdetails'), nullable=True)
    iddirection = db.Column(db.String(256), db.ForeignKey('directions.iddirection'), nullable=True)
    idworker = db.Column(db.Integer, db.ForeignKey('workers.idworker'), nullable=True)

    def __repr__(self):
        return '{numbercontract: %r,  datecontract: %r, typecontract: %r, periodcontract: %r, statuscontract: %r, valuecontract: %r, customerpassport: %r, iddirection: %r, idworker: %r}' % (
            self.numbercontract, self.datecontract, self.typecontract, self.statuscontract, self.valuecontract,
            self.customerpassport, self.iddirection, self.idworker)


class Pay(db.Model):
    __tablename__ = 'pay'
    accountnumber = db.Column(db.Integer, primary_key=True, nullable=True)
    paymentdate = db.Column(db.Date, nullable=True)
    paymentmethod = db.Column(db.String(256), nullable=True)
    numbercontract = db.Column(db.Integer, db.ForeignKey('contracts.numbercontract'), nullable=True)

    def __repr__(self):
        return '{accountnumber: %r,  paymentdate: %r, paymentmethod: %r, numbercontract: %r}' % (
        self.accountnumber, self.paymentdate, self.paymentmethod, self.numbercontract)
