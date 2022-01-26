from flasgger.utils import swag_from
from flask import jsonify
from flask import request
from flask_restx import Resource

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy
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
            print(check_password_hash(user.sign_password, str(self.password)))
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

class Worker:
    def __init__(self, id_worker, name_worker, post_worker,phone_number,login):
        self.id_worker = id_worker
        self.name_worker = name_worker
        self.post_worker = post_worker
        self.phone_number = phone_number
        self.login = login
    def add_info(self):
        new_worker = Workers(idworker=self.id_worker, nameworker=self.name_worker,
                                 postworker=self.post_worker, phonenumber=self.phone_number,
                                 login=self.login)

        app.session.add(new_worker)
        try:
            app.session.commit()
            return ''
        except SQLAlchemyError:
            app.session.rollback()
            return 'Произошла ошибка при добавлении в базу данных!'
class WorkerAPI(Resource):
    @swag_from("worker_json.yml")
    def post(self):
        id_worker = request.args.get("id_worker")
        name_worker = request.args.get("name_worker")
        post_worker = request.args.get("post_worker")
        phone_number = request.args.get("phone_number")
        login = request.args.get("login")

        worker = Worker(id_worker, name_worker, post_worker,phone_number,login)
        res = worker.add_info()
        return res

class Customer:
    def __init__(self, namecustomer, birthdaycustomer, passportdetails, login):
        self.namecustomer = namecustomer
        self.birthdaycustomer = birthdaycustomer
        self.passportdetails = passportdetails
        self.login = login
    def add_info(self):

        new_customer = Customers(namecustomer=self.namecustomer,
                                 birthdaycustomer=self.birthdaycustomer, passportdetails=self.passportdetails,
                                 login=self.login)

        app.session.add(new_customer)
        try:
            app.session.commit()
            return ''
        except SQLAlchemyError:
            app.session.rollback()
            return 'Произошла ошибка при добавлении в базу данных!'
class CustomerAPI(Resource):
    @swag_from("customer_json.yml")
    def post(self):
        namecustomer = request.args.get("namecustomer")
        birthdaycustomer = request.args.get("birthdaycustomer")
        passportdetails = request.args.get("passportdetails")
        login = request.args.get("login")
        customer = Customer(namecustomer, birthdaycustomer, passportdetails, login)
        res = customer.add_info()
        return res


class Contract:
    def __init__(self, login_user, login_customer, number_contract, date_contract, type_contract, period_contract,
                     status_contract, value_contract, id_direction):
        self.login_user = login_user
        self.login_customer = login_customer
        self.number_contract = number_contract
        self.date_contract = date_contract
        self.type_contract = type_contract
        self.period_contract = period_contract
        self.status_contract = status_contract
        self.value_contract = value_contract
        self.id_direction = id_direction

    def add_contract(self):
        passport_customer = app.session.query(Customers.passportdetails).filter_by(
            login=self.login_customer).scalar_subquery()
        id_worker = app.session.query(Workers.idworker).filter_by(login=self.login_user).scalar_subquery()
        new_contract = Contracts(numbercontract=self.number_contract, datecontract=self.date_contract,
                                 typecontract=self.type_contract, periodcontract=self.period_contract,
                                 statuscontract=self.status_contract, valuecontract=self.value_contract, iddirection=self.id_direction,
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

class ContractAPIGetInfo(Resource):
    @swag_from("contract_json_get.yml")
    def get(self):
        contracts = Contracts.query.all()

class ContractAPIAddContract(Resource):
    @swag_from("contract_json_post.yml")
    def post(self):
        login_user =  request.args.get("login_user")
        login_customer =  request.args.get("login_customer")
        number_contract =  request.args.get("number_contract")
        date_contract =  request.args.get("date_contract")
        type_contract =  request.args.get("type_contract")
        period_contract =  request.args.get("period_contract")
        status_contract =  request.args.get("status_contract")
        value_contract =  request.args.get("value_contract")
        id_direction =  request.args.get("id_direction")

        contract = Contract(login_user, login_customer, number_contract, date_contract, type_contract, period_contract,
                     status_contract, value_contract, id_direction)

        res = contract.add_info()
        return res

class ContractAPISetStatus(Resource):
    @swag_from("contract_json_patch.yml")
    def patch(self):
        start = request.args.get("DateContractStart")
        end = request.args.get("DateContractEnd")
        status = request.args.get("status")

        if (start > end):
            return 'Начало периода не может быть позже окончания периода!'
        else:
            app.session.execute(sqlalchemy.text("CALL update_status(:param1, :param2, :param3)"),
                                {"param1": status, "param2": start, "param3": end})
            try:
                app.session.commit()
                return jsonify({
                    "status": status
                })
            except SQLAlchemyError:
                return 'Произошла ошибка на стороне базы данных!'



class AddPay:
    def __init__(self, account_number, payment_method, payment_date, number_contract):
        self.account_number = account_number
        self.payment_method = payment_method
        self.payment_date = payment_date
        self.number_contract = number_contract

    def add_pay(self):
        new_pay = Pay(accountnumber=self.account_number, paymentmethod=self.payment_method,
                      paymentdate=self.payment_date, numbercontract=self.number_contract)
        try:
            app.session.add(new_pay)
            app.session.commit()
        except:
            return "Произошла ошибка!"

class PayAPIAddPay(Resource):

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

class PayAPIGetInfo(Resource):
    @swag_from("pay_json_get.yml")
    def get(self):
        pay = Pay.query.all()


# Api resource routing
api.add_resource(UserAPI, '/user/sign_in')
api.add_resource(ContractAPIGetInfo, '/contract/get_info')
api.add_resource(ContractAPIAddContract, '/contract/add_contract')
api.add_resource(ContractAPISetStatus, '/contract/set_status')
api.add_resource(PayAPIGetInfo, '/pay/get_info')
api.add_resource(PayAPIAddPay, '/pay/add_pay')
api.add_resource(WorkerAPI, '/worker/add_info')
api.add_resource(CustomerAPI, '/customer/add_info')
if __name__ == "__main__":
    app.run(debug=True)
