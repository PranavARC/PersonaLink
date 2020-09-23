from flask import Flask, request, redirect, url_for, render_template, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import functions

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=7)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    user = db.Column(db.String(100), primary_key=True)
    pwd = db.Column(db.String(100))
    mbti = db.Column(db.String(6))
    dnd = db.Column(db.String(15))
    types = db.Column(db.String(10))

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.mbti = "?"
        self.dnd = "?"
        self.types = "?"

@app.route('/', methods=['GET', 'POST'])
def main():
    if "user" in session:
        flash("You are already logged in")
        return redirect(url_for("profile"))

    if request.method == 'POST':
        session.permanent = True
        user = request.form["username"]
        password = request.form["password"]

        found_user = users.query.filter_by(user=user).first()

        if not(found_user):
            usr = users(user, password)
            db.session.add(usr)
            db.session.commit()
        else:
            if(found_user.pwd != password):
                flash("Incorrect password")
                return render_template("root.html")
        
        found_user = users.query.filter_by(user=user).first()

        session["user"] = user
        return redirect(url_for("profile"))
        """
        if(found_user):
            if(found_user.pwd == password):
                session["user"] = user
                session["password"] = password
                session["mbti"] = found_user.mbti
                session["dnd"] = found_user.dnd
                session["types"] = found_user.types
                return redirect(url_for("profile"))
            else:
                flash("Incorrect password")
        else:
            usr = users(user, password)
            db.session.add(usr)
            db.session.commit()
        """
    return render_template("root.html")

@app.route('/my-profile', methods=['GET', 'POST'])
def profile():
    if "user" in session:
        found_user = users.query.filter_by(user=session["user"]).first()
    else:
        flash("You need to log in")
        return redirect(url_for("main"))

    if request.method == 'POST':
        if request.form.get("logout"):
            session.clear()
            flash("You have logged out")
            return redirect(url_for("main"))
        elif request.form.get("mbti"):
            check = found_user.mbti = functions.detect(0)
        elif request.form.get("dnd"):
            check = found_user.dnd = functions.detect(1)
        elif request.form.get("type"):
            check = found_user.types = functions.detect(2)
            
        if(check != "?"):
            db.session.commit()
        else:
            flash("Something went wrong, please try again")
            db.session.rollback()

    arr = [found_user.user, found_user.pwd, found_user.mbti, found_user.dnd, found_user.types]
    return render_template("profile.html", arr = arr)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
