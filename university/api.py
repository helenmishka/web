from flasgger.utils import swag_from
from flask import jsonify
from flask import request
from flask_restx import Resource

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy

from university import app, api
from university.models import User, Contracts, Workers, Customers, Pay


class Users:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def sign_up(self):
            if self.login and self.password:
                user = User.query.filter_by(sign_login=self.login).first()

                if user and check_password_hash(user.sign_password, self.password):
                    if user.sign_role == 1:
                        global username
                        username = self.login
                        return 'user_space'
                    elif user.sign_role == 2:
                        return 'operator_space'
                    elif user.sign_role == 3:
                        return 'admin_space'
                else:
                    return jsonify('Неправильный логин или пароль!')
            else:
                return 'Нет логина или пароля!'

    def registration(self, password2, role):
        if not (self.login or self.password or password2):
            return 'Заполните все поля!'
        elif self.password != password2:
            return 'Пароли не совпадают'
        else:
            hash_password = generate_password_hash(self.password)
            new_user = User(sign_login=self.login, sign_password=hash_password, sign_role=role)
            app.session.add(new_user)
            app.session.commit()
class UserAPI(Resource):
    @swag_from("user_json.yml")
    def post(self):
        login = request.args.get("login")
        password = request.args.get("password")
        user = Users(login, password)
        res = user.sign_up()
        return res

class Contract:
    def add_contract(self, login_user, login_customer, number_contract, date_contract,type_contract,period_contract,status_contract,value_contract,id_direction):
        passport_customer = app.session.query(Customers.passportdetails).filter_by(login=login_customer).scalar_subquery()
        id_worker = app.session.query(Workers.idworker).filter_by(login=login_user).scalar_subquery()
        new_contract = Contracts(numbercontract=number_contract, datecontract=date_contract,
                                 typecontract=type_contract, periodcontract=period_contract,
                                 statuscontract=status_contract, valuecontract=value_contract, iddirection=id_direction,
                                 idworker=id_worker, customerpassport=passport_customer)

        app.session.add(new_contract)
        try:
            app.session.commit()
            return 'operator_space'
        except SQLAlchemyError:
            app.session.rollback()
            return 'Произошла ошибка при добавлении в базу данных!'

    def find_record(self, number_contract):
        rec = Contracts.query.filter_by(numbercontract=number_contract).all()
        return rec


class AddPay:
    def __init__(self, account_number, payment_method, payment_date, number_contract):
        self.account_number = account_number
        self.payment_method = payment_method
        self.payment_date = payment_date
        self.number_contract = number_contract

    def add_pay(self):
        new_pay = Pay(accountnumber = self.account_number, paymentmethod = self.payment_method, paymentdate = self.payment_date, numbercontract = self.number_contract)
        try:
            app.session.add(new_pay)
            app.session.commit()
        except:
            return "Произошла ошибка!"

class PayAPI(Resource):

    @swag_from("pay_json_post.yml")
    def post(self):
        account_number = request.args.get("pay_accountnumber")
        payment_method = request.args.get("pay_paymentmethod")
        payment_date = request.args.get("pay_paymentdate")
        number_contract = request.args.get("pay_numbercontract")
        pay = AddPay(account_number, payment_method, payment_date, number_contract)
        pay.add_pay()
        return jsonify({
            "accountnumber": account_number,
            "paymentmethod": payment_method,
            "paymentdate": payment_date,
            "numbercontract": number_contract
        })

    @swag_from("pay_json_get.yml")
    def get(self):
        pay = Pay.query.all()

## Api resource routing
api.add_resource(UserAPI, '/user')
api.add_resource(PayAPI, '/pay')

if __name__ == "__main__":
    app.run(debug=True)