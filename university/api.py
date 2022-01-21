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
from university.models import User, Contracts, Workers, Customers


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

class Contract:
    def add_contract(self, login_user, login_customer, number_contract, date_contract, type_contract, period_contract,
                     status_contract, value_contract, id_direction):
        passport_customer = app.session.query(Customers.passportdetails).filter_by(
            login=login_customer).scalar_subquery()
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

class ContractAPI(Resource):
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

    @swag_from("contract_json_post.yml")
    def post(self):
        number_contract = request.args.get("numbercontract")
        status_contract = request.args.get("statuscontract")
        customer_passport = request.args.get("customerpassport")

        contract = Contract.add_contract()
        return jsonify({
            "numbercontract": number_contract,
            "statuscontract": status_contract,
            "customerpassport": customer_passport
        })
    @swag_from("contract_json_get.yml")
    def get(self):
        contracts = Contracts.query.all()

# Api resource routing
api.add_resource(UserAPI, '/user')
api.add_resource(ContractAPI, '/contract')
if __name__ == "__main__":
    app.run(debug=True)
