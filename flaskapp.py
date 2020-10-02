from flask import Flask, request, redirect, url_for, render_template, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import functions

# Flask and SQLAlchemy code
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
        return redirect(url_for("profile", name=session["user"]))

    if request.method == 'POST':
        session.permanent = True
        user = (request.form["username"]).strip()
        password = request.form["password"].strip()
        if(user == "" or password == ""):
            flash("Please fill out both fields")
            return redirect(url_for("main"))
        if(user.find(" ") != -1):
            flash("No whitespace allowed in username")
            return redirect(url_for("main"))

        foundUser = users.query.filter_by(user=user.lower()).first()
        if not(foundUser):
            usr = users(user.lower(), password)
            db.session.add(usr)
            db.session.commit()
        else:
            if(foundUser.pwd != password):
                flash("Incorrect password")
                return render_template("login.html")
        
        foundUser = users.query.filter_by(user=user.lower()).first()

        session["user"] = user.lower()
        return redirect(url_for("profile", name=user))
    return render_template("login.html")

@app.route('/<name>', methods=['GET', 'POST'])
def profile(name):
    check = ""
    status = 0
    if "user" not in session:
        status = 1
    elif session["user"] != name.lower():
        status = 2

    foundUser = users.query.filter_by(user=name.lower()).first()

    if request.method == 'POST':
        if status == 1:
            flash("Please log in")
            return redirect(url_for("main"))
        elif status == 2:
            flash("You have reached your own account")
            return redirect(url_for("profile", name=session["user"]))

        if request.form.get("logout"):
            session.clear()
            flash("You have logged out")
            return redirect(url_for("main"))
        elif request.form.get("mbti"):
            return redirect(url_for("mbtiPg", name=name))
        elif request.form.get("dnd"):
            return redirect(url_for("dndPg", name=name))
        elif request.form.get("type"):
            return redirect(url_for("gramPg", name=name))

    # Errors pile up from arr without this,
    # likely because the compiler has a possibility of checking a none-type
    arr = ["", "", "", "", "", ""]
    if(foundUser is not None):
        arr = [name, foundUser.mbti, foundUser.dnd, foundUser.types, "Logout", foundUser.pwd]

    if status > 0:
        arr[5] = "***"
        if status == 1:
            arr[4] = "Login"
        else:
            arr[4] = "Your profile"
        return render_template("stranger.html", arr = arr)
    return render_template("profile.html", arr = arr)


@app.route('/<name>-mbti', methods=['GET', 'POST'])
def mbtiPg(name):
    if "user" not in session:
        flash("Please log in")
        return redirect(url_for("main"))
    elif session["user"] != name.lower():
        flash("Invalid page")
        return redirect(url_for("profile", name=session["user"]))

    check = "?"
    arr = []
    nums = []

    if request.method == 'POST':
        opinions = []
        for i in range(60):
            opinions.append(int(request.form["opinion"+str(i)]))
        # print(opinions)
        driverM = functions.headless(0)
        try:
            check = functions.mbtiSubmit(driverM, opinions)
        except:
            flash("Something went wrong, please try again")
            driverM.quit()
            return redirect(url_for("profile", name=session["user"]))

        driverM.quit()
        foundUser = users.query.filter_by(user=name.lower()).first()
        foundUser.mbti = check
        db.session.commit()
        flash("Your MBTI type is " + check)
        return redirect(url_for("profile", name=session["user"]))

    driver = functions.headless(0)
    arr = functions.mbtiScrape(driver)
    driver.quit()
    j = 0
    for i in arr:
        nums.append(j)
        j += 1
    return render_template("mbti.html", qs = arr, nums = nums)

@app.route('/<name>-dnd', methods=['GET', 'POST'])
def dndPg(name):
    if "user" not in session:
        flash("Please log in")
        return redirect(url_for("main"))
    elif session["user"] != name.lower():
        flash("Invalid page")
        return redirect(url_for("profile", name=session["user"]))

    check = "?"
    arr = []
    nums = []

    if request.method == 'POST':
        opinions = []
        for i in range(36):
            try:
                val = int(request.form["q"+str(i)])
            except:
                val = 0
            opinions.append(val)
        driverD = functions.headless(1)
        try:
            check = functions.dndSubmit(driverD, opinions)
        except:
            flash("Something went wrong, please try again")
            driverD.quit()
            return redirect(url_for("profile", name=session["user"]))
        
        driverD.quit()
        foundUser = users.query.filter_by(user=name.lower()).first()
        foundUser.dnd = check
        db.session.commit()
        flash("Your DND alignment is " + check)
        return redirect(url_for("profile", name=session["user"]))

    driver = functions.headless(1)
    arr = functions.dndScrape(driver)
    driver.quit()
    j = 0
    for i in arr:
        nums.append(j)
        j += 1
    return render_template("dnd.html", qs = arr, nums = nums)

@app.route('/<name>-gram', methods=['GET', 'POST'])
def gramPg(name):
    if "user" not in session:
        flash("Please log in")
        return redirect(url_for("main"))
    elif session["user"] != name.lower():
        flash("Invalid page")
        return redirect(url_for("profile", name=session["user"]))

    check = "?"
    arr = []
    nums = []

    if request.method == 'POST':
        opinions = [[], []]
        for i in range(52):
            val = request.form["q"+str(i)]
            title = val[:val.find("--")]
            val = int(val[-1])
            opinions[0].append(title)
            opinions[1].append(val)
        driverG = functions.headless(2)
        try:
            check = functions.gramSubmit(driverG, opinions)
        except:
            flash("Something went wrong, please try again")
            driverG.quit()
            return redirect(url_for("profile", name=session["user"]))
        
        driverG.quit()
        foundUser = users.query.filter_by(user=name.lower()).first()
        foundUser.types = check
        db.session.commit()
        flash("Your Enneagram type is " + check)
        return redirect(url_for("profile", name=session["user"]))
    
    driver = functions.headless(2)
    arr = functions.gramScrape(driver)
    driver.quit()
    j = 0
    for i in arr[0]:
        nums.append(j)
        j += 1    
    return render_template("gram.html", qs = arr, nums = nums)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)