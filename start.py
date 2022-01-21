from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from psycopg2 import *
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user
from collections import namedtuple
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime
from wtforms import SelectField
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = 'i love bmstu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:159357@localhost:5432/university_web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

Message = namedtuple('Message', 'text tag')
messages = []
SignUp = namedtuple('SignUp', 'login password')
log_and_pass = []

username = '0'

flag_space = 0

class Users(db.Model, UserMixin):
    __tablename__= 'users'
    login = db.Column(db.String(100), primary_key = True, nullable = True, unique = True)
    passworduser = db.Column(db.String(100), nullable=True)
    roleuser = db.Column(db.Integer, nullable=True)

    def get_id(self):
        return (self.login)

class Customers(db.Model):
    __tablename__ = 'customers'
    namecustomer = db.Column(db.String(256), nullable = True)
    birthdaycustomer = db.Column(db.Date, nullable = True)
    passportdetails = db.Column(db.Integer, nullable = True, primary_key= True)
    login = db.Column(db.String(256), db.ForeignKey('users.login'), nullable = True)

    def __repr__(self):
        return '<Directions %r>' % self.passportdetails

class Workers(db.Model):
    __tablename__ = 'workers'
    idworker = db.Column(db.Integer, primary_key=True, nullable=True)
    nameworker = db.Column(db.String(256), nullable = True)
    postworker = db.Column(db.String(256), nullable = True)
    phonenumber = db.Column(db.String(256), nullable = True)
    login = db.Column(db.String(256), db.ForeignKey('users.login'), nullable = True)

    def __repr__(self):
        return '<Directions %r>' % self.idworker


class Executors(db.Model):
    __tablename__ = 'executors'
    faculty = db.Column(db.String(256), nullable = True)
    department = db.Column(db.Integer, nullable = True)
    idexecutor = db.Column(db.Integer,nullable = True, primary_key= True)

    def __repr__(self):
        return '<Directions %r>' % self.idexecutor

class Directions(db.Model):
    __tablename__ = 'directions'
    typedirection= db.Column(db.String(256), nullable = True)
    iddirection = db.Column(db.String(256), primary_key= True, nullable = True)
    namedirection = db.Column(db.String(256), nullable = True)
    idexecutor = db.Column(db.Integer, db.ForeignKey('executors.idexecutor'), nullable = True)

    def __repr__(self):
        return '<Directions %r>' % self.iddirection
class Contracts(db.Model):
    __tablename__ = 'contracts'
    numbercontract = db.Column(db.Integer, primary_key= True, nullable = True)
    datecontract = db.Column(db.Date, nullable = True)
    typecontract = db.Column(db.String(256), nullable = True)
    periodcontract = db.Column(db.String(256), nullable = True)
    statuscontract = db.Column(db.String(256), nullable = True)
    valuecontract = db.Column(db.Integer, nullable = True)
    customerpassport = db.Column(db.Integer, db.ForeignKey('customers.passportdetails'), nullable = True)
    iddirection = db.Column(db.String(256), db.ForeignKey('directions.iddirection'), nullable = True)
    idworker = db.Column(db.Integer, db.ForeignKey('workers.idworker'), nullable = True)

    def __repr__(self):
        return '<Directions %r>' % self.numbercontract
class Pay(db.Model):
    __tablename__ = 'pay'
    accountnumber = db.Column(db.Integer, primary_key= True, nullable = True)
    paymentdate= db.Column(db.Date, nullable = True)
    paymentmethod = db.Column(db.String(256), nullable = True)
    numbercontract = db.Column(db.Integer, db.ForeignKey('contracts.numbercontract'), nullable = True)

    def __repr__(self):
        return '<Directions %r>' % self.accountnumber
@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/', methods = ['GET'])
def hello_world():
    return render_template('index.html')
@app.route('/main', methods = ['GET'])
def main():
    return render_template('main.html', messages = messages)

@app.route('/workers', methods = ['GET'])
def workers():
    worker = Workers.query.all()
    return render_template('workers.html', worker = worker)

@app.route('/contacts', methods = ['GET'])
def contacts():
    return render_template('contacts.html', messages = messages)

@app.route('/directions', methods = ['GET'])
def directions():
    dir = Directions.query.all()
    return render_template('directions.html', dir = dir)

@app.route('/user_space', methods = ['GET'])
def user_space():
    return render_template('user_space.html', messages = messages)

@app.route('/operator_space', methods = ['GET'])
def operator_space():
    return render_template('operator_space.html', messages = messages)

@app.route('/admin_space', methods = ['GET'])
def admin_space():
    return render_template('admin_space.html', messages = messages)
@app.route('/del_contract', methods = ['GET', 'POST'])
def del_contract():
    if request.method == 'POST':
        number_contract = request.form["NumberContract"]
        del_account = Pay.query.filter_by(numbercontract=number_contract).delete()
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash("Ошибка при удалении счета из базы данных!")
            return render_template('del_contract.html', messages = messages)
        del_contract = Contracts.query.filter_by(numbercontract = number_contract).delete()
        try:
            db.session.commit()
            return redirect(url_for('operator_space'))
        except SQLAlchemyError:
            db.session.rollback()
            flash("Ошибка при удалении договора из базы данных!")
            return render_template('del_contract.html', messages=messages)
    else:
        return render_template('del_contract.html', messages = messages)

@app.route('/del_contract_admin', methods = ['GET', 'POST'])
def del_contract_admin():
    if request.method == 'POST':
        number_contract = request.form["NumberContract"]
        del_account = Pay.query.filter_by(numbercontract=number_contract).delete()
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash("Ошибка при удалении счета из базы данных!")
            return render_template('del_contract_admin.html', messages=messages)
        del_contract = Contracts.query.filter_by(numbercontract=number_contract).delete()
        try:
            db.session.commit()
            return redirect(url_for('operator_space'))
        except SQLAlchemyError:
            db.session.rollback()
            flash("Ошибка при удалении договора из базы данных!")
            return render_template('del_contract_admin.html', messages=messages)
    else:
        return render_template('del_contract_admin.html', messages=messages)
@app.route('/add_new_pay', methods = ['GET', 'POST'])
def add_new_pay():
    global username
    if request.method == 'POST':
        account_number = request.form["AccountNumber"]
        payment_method = request.form.get("PaymentMethod")
        payment_date = request.form["PaymentDate"]
        number_contract = request.form["NumberContract"]
        payment_date= date.fromisoformat(payment_date)

        if not(account_number.isdigit() and int(account_number) > 0):
            flash("Неверный номер счета! Номер вводится в числовом формате")
        elif not(number_contract.isdigit() and int(number_contract) > 0):
            flash("Неверный номер договора! Номер вводится в числовом формате")
        else:
            new_pay = Pay(accountnumber = int(account_number), paymentmethod = payment_method, paymentdate = payment_date, numbercontract = int(number_contract))
            db.session.add(new_pay)
            try:
                db.session.commit()
                return redirect(url_for('operator_space'))
            except SQLAlchemyError:
                db.session.rollback()
                flash("Произошла ошибка при добавлении в базу данных!")
    return render_template('add_new_pay.html', messages = messages)
@app.route('/add_new_contract', methods = ['GET', 'POST'])
def add_new_contract():
    global username
    if request.method == 'POST':
        login_customer = request.form['login_customer']
        number_contract = request.form["NumberContract"]
        date_contract = request.form["DateContract"]
        type_contract = request.form.get("TypeContract")
        period_contract = request.form["PeriodContract"]
        status_contract = request.form.get("StatusContract")
        value_contract = request.form["ValueContract"]
        id_direction = request.form["IdDirection"]
        if not(number_contract.isdigit() and int(number_contract) > 0):
            flash("Неверный номер договора! Номер вводится в числовом формате")
        if not(value_contract.isdigit() and int(value_contract) > 0):
            flash("Стоимость вводится в числовом формате")
        else:
            date_contract_str = date.fromisoformat(date_contract)
            passport_customer = db.session.query(Customers.passportdetails).filter_by(login=login_customer).scalar_subquery()
            id_worker = db.session.query(Workers.idworker).filter_by(login=username).scalar_subquery()
            new_contract = Contracts(numbercontract = number_contract, datecontract = date_contract_str, typecontract = type_contract, periodcontract = period_contract, statuscontract = status_contract, valuecontract = value_contract, iddirection = id_direction, idworker = id_worker, customerpassport = passport_customer)

            db.session.add(new_contract)
            try:
                db.session.commit()
                return redirect(url_for('operator_space'))
            except SQLAlchemyError:
                db.session.rollback()
                flash("Произошла ошибка при добавлении в базу данных!")

    return render_template('add_new_contract.html', messages = messages)


@app.route('/new_status', methods = ['GET', 'POST'])
def new_status():
    if request.method == 'POST':
        start = request.form["DateContractStart"]
        end = request.form["DateContractEnd"]
        status = request.form.get("StatusContract")
        start = date.fromisoformat(start)
        end = date.fromisoformat(end)
        if (start > end):
            flash("Начало периода не может быть позже окончания периода!")
        else:
            db.session.execute(sqlalchemy.text("CALL update_status(:param1, :param2, :param3)"),{"param1": status, "param2": start, "param3": end})
            try:
                db.session.commit()
                return redirect(url_for('operator_space'))
            except SQLAlchemyError:
                flash("Произошла ошибка на стороне базы данных!")
    return render_template('new_status.html', messages = messages)


@app.route('/customer_contract', methods = ['GET'])
def customer_contract():
    global username
    passport_customer = db.session.query(Customers.passportdetails).filter_by(login=username).scalar_subquery()
    query = db.session.query(Contracts, Customers).filter_by(customerpassport = passport_customer)
    query = query.join(Customers, Customers.passportdetails == Contracts.customerpassport)
    print(query)
    con = query.all()
    return render_template('customer_contract.html', con=con)

@app.route('/sort_contract', methods = ['GET', 'POST'])
def sort_contract():
    global username
    check = request.form.get('check')
    if request.method == 'POST':
        check = int(check)
        passport_customer = db.session.query(Customers.passportdetails).filter_by(login=username).scalar_subquery()
        if (check == 1):
            con = Contracts.query.filter_by(customerpassport=passport_customer).order_by(Contracts.datecontract)
            return render_template('contract.html', con=con)
        elif (check == 2):
            con = Contracts.query.filter_by(customerpassport=passport_customer).order_by(Contracts.typecontract)
            return render_template('contract.html', con=con)
        elif (check == 3):
            con = Contracts.query.filter_by(customerpassport=passport_customer).order_by(Contracts.periodcontract)
            return render_template('contract.html', con=con)
        elif (check == 4):
            con = Contracts.query.filter_by(customerpassport=passport_customer).order_by(Contracts.statuscontract)
            return render_template('contract.html', con=con)
    else:
        return render_template('sort_contract.html',messages=messages)
@app.route('/filt_contract', methods = ['GET', 'POST'])
def filt_contract():
    global username
    if request.method == 'POST':
        date_check = request.form.get('check_1')
        type_check = request.form.get('check_2')
        period_check = request.form.get('check_3')
        status_check = request.form.get('check_4')
        date_contract = request.form["Date"]
        type_contract = request.form.get("Type")
        period_contract = request.form["Period"]
        status_contract = request.form.get("Status")
        passport_customer = db.session.query(Customers.passportdetails).filter_by(login=username).scalar_subquery()
        con = Contracts.query.filter_by(customerpassport=passport_customer)
        if(date_check):
            con = con.filter_by(datecontract = date_contract)
        if(type_check):
            con = con.filter_by(typecontract = type_contract)
        if (period_check):
            con = con.filter_by(periodcontract=period_contract)
        if (status_check):
            con = con.filter_by(statuscontract=status_contract)
        return render_template('contract.html', con=con)

    return render_template('filt_contract.html',messages=messages)

@app.route('/search_contract', methods = ['GET', 'POST'])
def search_contract():
    search_contract = request.form.get('search_contract')
    query = db.session.query(Contracts, Customers).filter_by(numbercontract = search_contract)
    query = query.join(Customers, Customers.passportdetails == Contracts.customerpassport)
    con = query.all()
    pay = 'Не оплачен'
    for c, ct in con:
        acc = Pay.query.filter_by(numbercontract = c.numbercontract).all()
        if len(acc) != 0:
            for p in acc:
                pay = p.accountnumber
    return render_template('search_contract.html', con=con, pay=pay)

class Form(FlaskForm):
    name = SelectField('name',choices = [])

@app.route('/lk_space', methods=['GET'])
def lk_space():
    global flag_space
    if flag_space == 1:
        return redirect(url_for('user_space'))
    elif flag_space == 2:
        return redirect(url_for('operator_space'))
    elif flag_space == 3:
        return redirect(url_for('admin_space'))
    else:
        return render_template('lk_space.html', messages=messages)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    login = request.form.get('login')
    password = request.form.get('password')
    global flag_space
    global username
    if request.method == 'POST':
        if login and password:
            user = Users.query.filter_by(login = login).first()
            if user and check_password_hash(user.passworduser, password):
                login_user(user)
                if user.roleuser == 1:
                    username = login
                    flag_space = 1
                    return redirect(url_for('user_space'))
                elif user.roleuser == 2:
                    username = login
                    flag_space = 2
                    return redirect(url_for('operator_space'))
                elif user.roleuser == 3:
                    username = login
                    flag_space = 3
                    return redirect(url_for('admin_space'))
            else:
                flash('Неправильный логин или пароль!')
        else:
            flash('Нет логина или пароля!')
    return render_template('sign_up.html', messages=messages)


@app.route('/log_out', methods=['GET', 'POST'])
@login_required
def log_out():
    global flag_space
    logout_user()
    global username
    username = '0'
    flag_space = 0
    return redirect(url_for('hello_world'))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    role = request.form.get('role')
    if request.method == 'POST':
        role = int(role)
        if (role == 1):
            return render_template('registration_user.html', messages = messages)
        elif(role == 2):
            return render_template('registration_worker.html', messages = messages)
        elif(role == 3):
            return render_template('registration_admin.html', messages = messages)
    return render_template('registration.html', messages=messages)

@app.route('/registration_user', methods=['GET', 'POST'])
def registration_user():
    name_customer = request.form.get('name_customer')
    birthday = request.form.get('birthday')
    passport = request.form.get('passport')
    login = request.form.get('reg_login')
    password1 = request.form.get('reg_password1')
    password2 = request.form.get('reg_password2')

    if request.method == 'POST':
        if not (login or password1 or password2 or name_customer or birthday or passport):
            flash('Заполните все поля!')
        if not (passport.isdigit()):
            flash('Неверный номер паспорта', category='error')
        elif password1 != password2:
            flash('Пароли не совпадают')
        else:
            hash_password = generate_password_hash(password1)
            new_user = Users(login=login, passworduser=hash_password, roleuser=1)
            birthday_str = date.fromisoformat(birthday)
            new_customer = Customers(namecustomer=name_customer, birthdaycustomer=birthday_str,
                                     passportdetails=int(passport), login=login)

            db.session.add(new_user)
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                flash("Произошла ошибка при добавлении в базу данных!")
            db.session.add(new_customer)
            try:
                db.session.commit()
                flash("Пользователь успешно зарегистрирован!")
                return render_template('sign_up.html', messages=messages)
            except SQLAlchemyError:
                db.session.rollback()
                del_user = Users.query.filter_by(login=login).delete()
                db.session.commit()
                flash("Произошла ошибка при добавлении в базу данных!")
    return render_template('registration_user.html', messages=messages)

@app.route('/registration_worker', methods=['GET', 'POST'])
def registration_worker():
    id_worker = request.form.get('id_worker')
    name_worker = request.form.get('name_worker')
    post_worker = request.form.get('post_worker')
    phone = request.form.get('phone_number')
    login = request.form.get('reg_login')
    password1 = request.form.get('reg_password1')
    password2 = request.form.get('reg_password2')

    if request.method == 'POST':
        if not (login or password1 or password2 or name_worker or id_worker or post_worker or phone):
            flash('Заполните все поля!')
        if not (id_worker.isdigit()):
            flash('Неверный номер паспорта')
        elif password1 != password2:
            flash('Пароли не совпадают')
        else:
            hash_password = generate_password_hash(password1)
            new_user = Users(login=login, passworduser=hash_password, roleuser=2)
            db.session.add(new_user)
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                flash("Произошла ошибка при добавлении в базу данных!")
            new_worker = Workers(idworker=id_worker, nameworker=name_worker, postworker=post_worker, phonenumber=phone,
                                 login=login)
            db.session.add(new_worker)
            try:
                db.session.commit()
                flash("Пользователь успешно зарегистрирован!")
                return render_template('sign_up.html', messages=messages)
            except SQLAlchemyError:
                db.session.rollback()
                del_user = Users.query.filter_by(login=login).delete()
                db.session.commit()
                flash("Произошла ошибка при добавлении в базу данных!")
    return render_template('registration_worker.html', messages=messages)

@app.route('/registration_admin', methods=['GET', 'POST'])
def registration_admin():
    login = request.form.get('reg_login')
    password1 = request.form.get('reg_password1')
    password2 = request.form.get('reg_password2')

    if request.method == 'POST':
        if not (login or password1 or password2):
            flash('Заполните все поля!')
        elif password1 != password2:
            flash('Пароли не совпадают')
        else:
            hash_password = generate_password_hash(password1)
            new_user = Users(login=login, passworduser=hash_password, roleuser=3)
            db.session.add(new_user)
            try:
                db.session.commit()
                flash("Пользователь успешно зарегистрирован!")
                return render_template('sign_up.html', messages=messages)
            except SQLAlchemyError:
                db.session.rollback()
                flash("Произошла ошибка при добавлении в базу данных!")
    return render_template('registration_worker.html', messages=messages)








