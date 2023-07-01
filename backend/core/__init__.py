from flask import Flask
from .config import load_config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(load_config())
db = SQLAlchemy(app)
Swagger(app)
CORS(app, origins=['*'])