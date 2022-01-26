from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_restx import Api, Resource, fields
from flasgger import Swagger
import config


app = Flask(__name__)
app.secret_key = 'i love bmstu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:159357@localhost:5432/university_web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create an APISpec
template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask Restful Swagger",
        "description": "Dima and Lena, BMSTU",
        "version": "0.1.1",
        "contact": {
            "name": "Dima and Lena",
            "url": "",
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": ["123"]
        }
    ]

}

app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3,
    "specs_route": "/"
}
swagger = Swagger(app, template=template)
app.config.from_object(config.Config)
api = Api(app)
