import datetime
from functools import wraps
from hashlib import md5
import random
from sqlite3 import IntegrityError
from flask import abort, flash, g, redirect, render_template, request, session, url_for
from app import app, database
from app.models import Account, Customer, Transaction


# ready
@app.before_request
def before_request():
    g.db = database
    g.db.connect()


# ready
@app.after_request
def after_request(response):
    g.db.close()
    return response


# ready
@app.context_processor
def _inject_user():
    return {"current_user": get_current_user()}


# ready
def auth_user(user):
    try:
        session["logged_in"] = True
        session["user_id"] = user.id
        session["username"] = user.username
        session["accnum"] = user.account.accnum
        flash("Bienvenido: %s" % (user.username))
    except:
        return redirect(url_for("homepage"))


# ready
def get_current_user():
    try:
        if session.get("logged_in"):
            return Customer.get(Customer.id == session["user_id"])
    except:
        logout()


# ready
@app.route("/")
def homepage():
    if session.get("logged_in"):
        return transactions()
    else:
        return render_template("public.html")


# ready
def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return inner


# ready
@app.route("/logout/")
def logout():
    session.pop("logged_in", None)
    flash("La sesión ha terminado")
    return redirect(url_for("homepage"))


# ready
def object_list(template_name, qr, var_name="object_list", **kwargs):
    kwargs.update(page=int(request.args.get("page", 1)), pages=qr.count() / 20 + 1)
    kwargs[var_name] = qr.paginate(kwargs["page"])
    return render_template(template_name, **kwargs)


# ready
@app.route("/join/", methods=["GET", "POST"])
def join():
    if request.method == "POST" and request.form["username"]:
        try:
            with database.atomic():
                user = Customer.create(
                    username=request.form["username"],
                    password=md5(
                        (request.form["password"]).encode("utf-8")
                    ).hexdigest(),
                    created_at=datetime.datetime.now(),
                )
                Account.create(
                    customer_id=user.id,
                    accnum=random.randint(100000, 200000),
                    pin=random.randint(2000, 3000),
                    balance=0.0,
                    created_at=datetime.datetime.now(),
                )

            auth_user(user)
            redirect(url_for("atm"))

        except IntegrityError:
            flash("Alguién más está usando ese nick")

    return render_template("join.html")


# ready
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST" and request.form["username"]:
        try:
            pw_hash = md5(request.form["password"].encode("utf-8")).hexdigest()
            user = Customer.get(
                (Customer.username == request.form["username"])
                & (Customer.password == pw_hash)
            )
        except Customer.DoesNotExist:
            flash("Credenciales incorrectas")
        else:
            auth_user(user)
            redirect(url_for("atm"))

    return render_template("login.html")


# ready
@app.route("/account/")
def account():
    user = get_current_user()

    try:
        account = user.account.get()
        return render_template("account.html", account=account)
    except:
        return redirect(url_for("homepage"))


# ready
@app.route("/transactions/")
def transactions():
    user = get_current_user()

    try:
        transactions = user.transactions
        return object_list("transactions.html", transactions, "transactions")
    except:
        return redirect(url_for("homepage"))

    # ready


@app.route("/atm", methods=["GET", "POST"])
@login_required
def atm():
    return render_template("atm.html")


@app.route("/withdraw/", methods=["GET", "POST"])
@login_required
def withdraw():
    user = get_current_user()
    if request.method == "POST" and request.form["amount"]:
        Transaction.create(
            customer=user,
            to_accnum=user.account.get().accnum,
            ttype="RETIRO",
            amount=request.form["amount"],
            p_balance=user.account.get().balance,
            c_balance=user.account.get().balance + float(request.form["amount"]),
            completed=False,
            created_at=datetime.datetime.now(),
        )
        flash("Se ha puesta en cola el retiro con monto: $" + request.form["amount"])

    return render_template("create.html", account=user.account.first().accnum)


@app.route("/atm-credit/", methods=["GET", "POST"])
def atm_transaction():
    user = get_current_user()
    if request.method == "POST":
        data = request.get_json()
        Transaction.create(
            customer=user,
            to_accnum=user.account.get().accnum,
            ttype="DEPOSITO",
            amount=float(data["amount"]),
            p_balance=user.account.get().balance,
            c_balance=user.account.get().balance + float(data["amount"]),
            completed=True,
            created_at=datetime.datetime.now(),
        )
        Account.update(
            customer_id=user.id,
            balance=float(data["amount"]),
        )

    results = {"completed": 1}

    return results


# Vicente

# Aquí va la implementación de Threads
# ####### import multiprocessing # #######

# @app.route("/makewithdraw/<transaction_id>/")
# def make_withdraw(transaction_id):
#     transaction = (
#         Transaction.select()
#         .where(Transaction.id == transaction_id)
#         .order_by(Transaction.customer)
#     )
#     from_account = transaction.get().from_account

#     queue = multiprocessing.Queue()

#     def process_transaction(transaction_id):
#         queue.put(transaction_id)

#     processes = []
#     for i in range(5):
#         process = multiprocessing.Process(target=process_transaction, args=(transaction_id,))
#         processes.append(process)
#         process.start()

#     for process in processes:
#         process.join()

#     while not queue.empty():
#         transaction_id = queue.get()
#         print(transaction_id)

#     return render_template("atm.html")
### ===========import threading # ####### =================================
#  import threading

# @app.route("/makewithdraw/<transaction_id>/")
# def make_withdraw(transaction_id):
#     transaction = (
#         Transaction.select()
#         .where(Transaction.id == transaction_id)
#         .order_by(Transaction.customer)
#     )
#     from_account = transaction.get().from_account

#     queue = []

#     def thread_transaction(transaction_id):
#         queue.append(transaction_id)

#     threads = []
#     for i in range(5):
#         thread = threading.Thread(target=thread_transaction, args=(transaction_id,))
#         threads.append(thread)
#         thread.start()

#     for thread in threads:
#         thread.join()

#     for transaction_id in queue:
#         print(transaction_id)

#     return render_template("atm.html")

###====== ===========End threading # ####### =================================
