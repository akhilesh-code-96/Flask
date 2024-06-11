from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
from dotenv import load_dotenv
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.getenv('api_key')
app.permanent_session_lifetime = timedelta(minutes=5)


def configure():
  load_dotenv()
  
  
def connect_db():
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=os.getenv('password'),
  database="flask_db"
  )
  cur = mydb.cursor()
  
  return mydb, cur


@app.route("/")
def home():
  if 'isLoggedIn' in session and session['isLoggedIn'] == "True":
    return redirect(url_for("afterlogin"))
  else:
	  return render_template("index.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
  if request.method == 'POST':
    email = request.form.get('floating_email')
    password = request.form.get('floating_password')
    first_name = request.form.get('floating_first_name')
    last_name = request.form.get('floating_last_name')
    phone = request.form.get('floating_phone')
    company = request.form.get('floating_company')
    
    db, cur = connect_db()
    cmd = f"insert into info values('{first_name}', '{last_name}', '{email}', '{password}', '{phone}', '{company}')"
    cur.execute(cmd)
    db.commit()
    return redirect(url_for("thanks"))
  return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form["email"]
    password = request.form["password"]
    
    db, cur = connect_db()
    cmd = f"select * from info where email_address = '{email}' AND password = '{password}'"
    cur.execute(cmd)
    result = cur.fetchone()
    
    if result:
      session.permanent = True
      session["email"] = email
      session["isLoggedIn"] = "True"
      return redirect(url_for("afterlogin"))
    else:
      return "Please check your email or password"
  else:
    if 'isLoggedIn' in session and session['isLoggedIn'] == "True":
      return redirect(url_for("afterlogin"))
    return render_template("index.html")


@app.route("/afterlogin")
def afterlogin():
  if 'isLoggedIn' in session and session['isLoggedIn'] == "True":
    return render_template("login.html")
  else:
    return redirect(url_for("home"))
  
@app.route("/thanks")
def thanks():
  return render_template("thanks.html")
  
@app.route("/logout", methods=["POST"])
def logout():
  session.pop("email", None)
  session.pop("isLoggedIn", None)
  return redirect(url_for("home"))


if __name__ == '__main__':
  configure()
  app.run(debug=True)