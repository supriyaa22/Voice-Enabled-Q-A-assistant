from flask import (
    Flask,
    render_template,
    request
)
from flask_sqlalchemy import SQLAlchemy
import os
import pytz
from datetime import datetime, timedelta
from qa import q_and_a
from summary import run_summarization
from image_to_text import convert_image_to_text
from PIL import Image
from text_to_speech import text_to_speech

#
global_user_id = None
#

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.sqlite"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["WHOOSH_BASE"] = "whoosh"
app.config["SECRET_KEY"] = "thisissecret"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)

db = SQLAlchemy(app)

IST = pytz.timezone("Asia/Kolkata")


class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    role = db.Column(db.String(30))

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role


class QA(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    text = db.Column(db.Text)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)

    def __init__(self, user_id, text, question, answer):
        self.user_id = user_id
        self.text = text
        self.question = question
        self.answer = answer


class TS(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    text = db.Column(db.Text)
    summary = db.Column(db.Text)

    def __init__(self, user_id, text, summary):
        self.user_id = user_id
        self.text = text
        self.summary = summary


db.create_all()


@app.route("/")
def index():
    return render_template("login.html", template_folder="templates")


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("signup_username")
    check_username = Users.query.filter_by(username=username).first()
    if check_username:
        return {"error": "user already exists"}
    email = request.form.get("signup_email")
    check_email = Users.query.filter_by(email=email).first()
    if check_email:
        return {"error": "email already exists"}
    password = request.form.get("signup_password")
    cpassword = request.form.get("signup_cpassword")
    role = "user"
    if password == cpassword:
        new_user = Users(username, email, password, role)
        db.session.add(new_user)
        db.session.commit()
        return render_template("profile.html", template_folder="templates")
    else:
        return {"error": "password does not match"}


@app.route("/signin", methods=["POST"])
def signin():
    global global_user_id
    username = request.form.get("signin_username")
    password = request.form.get("signin_password")
    user = Users.query.filter_by(username=username).first()
    if user == None:
        return {"error": "user not found"}
    validate = Users.query.filter_by(username=username, password=password).first()
    if validate != None:
        if validate.role == "user":
            global_user_id = user.id
            return render_template("profile.html", template_folder="templates")
        elif validate.role == "admin":
            return {"hi": username, "role": "admin"}
    else:
        return {"error": "wrong password"}


@app.route("/h", methods=["GET"])
def h():
    return render_template("profile.html", template_folder="templates")


@app.route("/a", methods=["GET"])
def a():
    return render_template("QA.html", template_folder="templates")


@app.route("/qa", methods=["POST"])
def qa():
    global global_user_id
    context = request.form.get("paragraph_text")
    file = request.form.get("pic")
    if file:
        print(file)
        context = convert_image_to_text(file)
        print(context)
    question = request.form.get("question")
    answer = q_and_a(context, question)
    qa_data = QA(global_user_id, context, question, answer)
    db.session.add(qa_data)
    db.session.commit()
    return render_template(
        "QA.html",
        template_folder="templates",
        answer=answer,
        context=context,
        question=question,
    )


@app.route("/qa_history", methods=["GET"])
def qa_history():
    all_data = QA.query.filter_by(user_id=global_user_id).all()
    return render_template(
        "QAhistory.html", template_folder="templates", all_data=all_data
    )


@app.route("/b", methods=["GET"])
def b():
    return render_template("TS.html", template_folder="templates")


@app.route("/ts", methods=["POST"])
def ts():
    global global_user_id
    context = request.form.get("paragraph_text")
    print(context)
    # print(type(context))
    file = request.form.get("pic")
    print("file_name : ", file)
    if file:
        print(file)
        context = convert_image_to_text(file)
        print(context)

    answer = run_summarization(context)
    ts_data = TS(global_user_id, context, answer)
    db.session.add(ts_data)
    db.session.commit()
    return render_template(
        "TS.html", template_folder="templates", answer=answer, context=context
    )


@app.route("/ts_history", methods=["GET"])
def ts_history():
    all_data = TS.query.filter_by(user_id=global_user_id).all()
    return render_template(
        "TShistory.html", template_folder="templates", all_data=all_data
    )


@app.route("/qa_speech", methods=["POST"])
def qa_speech():
    answer = request.form.get("answer")
    text_to_speech(answer)
    return render_template(
        "QA.html",
        template_folder="templates",
        answer=answer,
        context='',
        question='',
    )

@app.route("/ts_speech", methods=["POST"])
def ts_speech():
    answer = request.form.get("answer")
    text_to_speech(answer)
    return render_template(
        "TS.html", template_folder="templates", answer=answer, context=''
    )


if __name__ == "__main__":
    app.run(debug=True)
