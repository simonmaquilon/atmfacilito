import datetime
from functools import wraps
from hashlib import md5
import random
from sqlite3 import IntegrityError
from flask import abort, flash, g, redirect, render_template, request, session, url_for
from app import app, database
from app.models import Account, Customer, Transaction
import urllib

queue = []


def my_url_for(request, name: str, **path_params) -> str:
    url = request.url_for(name, **path_params)
    parsed = list(urllib.parse.urlparse(url))
    parsed[1] = "localhost:3000"
    return urllib.parse.urlunparse(parsed)


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


def auth_user(user):
    session["logged_in"] = True
    session["user_id"] = user.id
    session["username"] = user.username
    flash("You are logged in as %s" % (user.username))


def get_current_user():
    if session.get("logged_in"):
        return Customer.get(Customer.id == session["user_id"])


@app.context_processor
def _inject_user():
    return {"current_user": get_current_user()}


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return inner


@app.route("/withdraw/", methods=["GET", "POST"])
@login_required
def withdraw():
    user = get_current_user()
    if request.method == "POST" and request.form["amount"]:
        transaction = Transaction.create(
            customer=user,
            from_account=user.account.get().account,
            to_account=user.account.get().account,
            ttype="RETIRO",
            amount=request.form["amount"],
            p_balance=user.account.get().balance,
            c_balance=user.account.get().balance + float(request.form["amount"]),
            created_at=datetime.datetime.now(),
        )
        flash("Se ha puesta en cola el retiro con monto:" + request.form["amount"])
        return redirect(url_for("atm"))  # , username=user.username))

    return render_template("create.html", account=user.account.first().account)


def object_list(template_name, qr, var_name="object_list", **kwargs):
    kwargs.update(page=int(request.args.get("page", 1)), pages=qr.count() / 20 + 1)
    kwargs[var_name] = qr.paginate(kwargs["page"])
    return render_template(template_name, **kwargs)


def get_object_or_404(model, *expressions):
    try:
        return model.get(*expressions)
    except model.DoesNotExist:
        abort(404)


# @app.template_filter("is_following")
# def is_following(from_user, to_user):
#     return from_user.is_following(to_user)


@app.route("/private/")
def private_timeline():
    user = get_current_user()
    transactions = user.transactions
    return object_list("private_messages.html", transactions, "message_list")


@app.route("/public/")
def public_timeline():
    transaction = Transaction.select().order_by(Transaction.customer.asc())
    return object_list("public_messages.html", transaction, "message_list")


@app.route("/")
def homepage():
    if session.get("logged_in"):
        return private_timeline()
        pass
    else:
        return public_timeline()


@app.route("/makewithdraw/<transaction_id>/")
def make_withdraw(transaction_id):  # , single, multi):
    transaction = (
        Transaction.select()
        .where(Transaction.id == transaction_id)
        .order_by(Transaction.customer)
    )
    print(transaction.get().from_account)
    # Thread.sleep(1000)

    queue.append(transaction_id)
    print(queue)

    return render_template("atm.html")

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


@app.route("/account/")
def my_account():
    user = get_current_user()
    account = user.account.get()

    return render_template("my_account.html", account=account)


@app.route("/atm/")
def atm():
    return render_template("atm.html")


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
                    account=random.randint(100000, 200000),
                    pin=random.randint(2000, 3000),
                    balance=0.0,
                    created_at=datetime.datetime.now(),
                )

            auth_user(user)
            return redirect(url_for("atm"))

        except IntegrityError:
            flash("Alguién más está usando ese nick")

    return render_template("join.html")


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
            return redirect(url_for("atm"))

    return render_template("login.html")


@app.route("/logout/")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("atm"))


# @app.route("/following/")
# @login_required
# def following():
#     user = get_current_user()
#     return object_list("user_following.html", user.following(), "user_list")


# @app.route("/followers/")
# @login_required
# def followers():
#     user = get_current_user()
#     return object_list("user_followers.html", user.followers(), "user_list")


@app.route("/users/")
def user_list():
    users = Customer.select().order_by(Customer.username)
    return object_list("user_list.html", users, "user_list")


@app.route("/users/<username>/")
def user_detail(username):
    user = get_object_or_404(Customer, Customer.username == username)

    # messages = user.transac.order_by(Message.pub_date.desc())
    return object_list("user_detail.html", """ messages, "message_list", user=user """)


# @app.route("/users/<username>/follow/", methods=["POST"])
# @login_required
# def user_follow(username):
#     user = get_object_or_404(User, User.username == username)
#     try:
#         with database.atomic():
#             Relationship.create(from_user=get_current_user(), to_user=user)
#     except IntegrityError:
#         pass

#     flash("You are following %s" % user.username)
#     return redirect(url_for("user_detail", username=user.username))


# @app.route("/users/<username>/unfollow/", methods=["POST"])
# @login_required
# def user_unfollow(username):
#     user = get_object_or_404(User, User.username == username)
#     (
#         Relationship.delete()
#         .where(
#             (Relationship.from_user == get_current_user())
#             & (Relationship.to_user == user)
#         )
#         .execute()
#     )
#     flash("You are no longer following %s" % user.username)
#     return redirect(url_for("user_detail", username=user.username))
