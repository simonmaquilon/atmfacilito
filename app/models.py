from peewee import (
    ForeignKeyField,
    DateTimeField,
    IntegerField,
    FloatField,
    CharField,
    TextField,
)
from app import BaseModel


class Customer(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField()

    # def following(self):
    #     return (
    #         User.select()
    #         .join(Relationship, on=Relationship.to_user)
    #         .where(Relationship.from_user == self)
    #         .order_by(User.username)
    #     )

    # def followers(self):
    #     return (
    #         User.select()
    #         .join(Relationship, on=Relationship.from_user)
    #         .where(Relationship.to_user == self)
    #         .order_by(User.username)
    #     )

    # def is_following(self, user):
    #     return (
    #         Relationship.select()
    #         .where((Relationship.from_user == self) & (Relationship.to_user == user))
    #         .exists()
    #     )

    # def gravatar_url(self, size=80):
    #     print(self.username)
    #     return (
    #         "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/%s.png"
    #         % (self.id + 2 if (self.id % 2) == 0 else self.id + 0)
    #     )

    # def transactions(self):
    #     return Transaction.select()


class Account(BaseModel):
    customer = ForeignKeyField(Customer, backref="account")
    account = CharField(unique=True)
    pin = CharField()
    balance = FloatField()
    created_at = DateTimeField()


class Transaction(BaseModel):
    customer = ForeignKeyField(Customer, backref="transactions")
    from_account = CharField()
    to_account = CharField()
    ttype = TextField()
    amount = FloatField()
    p_balance = FloatField()
    c_balance = FloatField()
    created_at = DateTimeField()
