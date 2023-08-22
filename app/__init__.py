from flask import Flask
from flask_qrcode import QRcode
from peewee import SqliteDatabase, Model
from os import environ
from dotenv import load_dotenv

load_dotenv()

DATABASE = environ.get("DATABASE")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
qrcode = QRcode(app)
app.config.update(SECRET_KEY=environ.get("SECRET_KEY"))

database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


from app import routes, models


def create_tables():
    with database:
        database.create_tables(
            [models.Account, models.Customer, models.Transaction], safe=True
        )
