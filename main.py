# import requests
# r = requests.get('https://google.com')

# print(r.status_code)

# import atmpkg.account.create_account as account

# account.register_customer()

# import sqlite3
# con = sqlite3.connect("data/database.sqlite")

# cur = con.cursor()

# # cur.execute("CREATE TABLE movie(title, year, score)")
# # cur.execute("""
# #     INSERT INTO movie VALUES
# #         ('Monty Python and the Holy Grail', 1975, 8.2),
# #         ('And Now for Something Completely Different', 1971, 7.5)
# # """)
# # con.commit()

# res = cur.execute("SELECT * FROM movie")
# print(res.fetchall())

# API de prueba
# from fastapi import FastAPI
# app = FastAPI()

# @app.get("/create-account")
# def hello():
#   return {"Account created!"}


# Interface UI de Prueba
from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Label, Static

class EditableText(Static):
    """Custom widget to show (editable) static text."""

    def compose(self) -> ComposeResult:
        yield Label()
        yield Input()
        yield Button()
        yield Button()

class EditableTextApp(App[None]):
    def compose(self) -> ComposeResult:
        yield EditableText()

app = EditableTextApp()

if __name__ == "__main__":
    app.run()