from peewee import (
    ForeignKeyField,
    DateTimeField,
    BooleanField,
    FloatField,
    CharField,
    TextField,
)
from app import BaseModel


class Customer(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField()

    def income_transactions(self):
        return Transaction.select().where(
            (Transaction.to_account == self.account.accnum)
        )

    def gravatar_url(self):
        return (
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/%s.png"
            % (self.id + 2 if (self.id % 2) == 0 else self.id + 0)
        )


class Account(BaseModel):
    customer = ForeignKeyField(Customer, backref="account")
    accnum = CharField(unique=True)
    pin = CharField()
    balance = FloatField()
    created_at = DateTimeField()


class Transaction(BaseModel):
    customer = ForeignKeyField(Customer, backref="transactions")
    to_accnum = CharField()
    ttype = TextField()
    amount = FloatField()
    p_balance = FloatField()
    c_balance = FloatField()
    completed = BooleanField()
    created_at = DateTimeField()
