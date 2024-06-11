from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "aldfkjladsfs"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    user = request.form["username"]
    if user:
      session.permanent = True
      session["username"] = user
      return redirect(url_for("user"))
    else:
      return "Please provide a username", 400
  else:
    if "username" in session:
      return redirect(url_for("user"))
    return render_template("login.html")


@app.route("/user")
def user():
  if "username" in session:
    user = session["username"]
    return f"<h1>{user}</h1>"
  else:
    return redirect(url_for("login"))
  
  
@app.route("/logout")
def logout():
  session.pop("username", None)
  return redirect(url_for("login"))


if __name__ == '__main__':
	app.run(debug=True)