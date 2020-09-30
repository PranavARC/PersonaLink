from flask import Flask, request, redirect, url_for, render_template, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import functions2

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
    types = db.Column(db.String(6))

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

        found_user = users.query.filter_by(user=user.lower()).first()
        if not(found_user):
            usr = users(user.lower(), password)
            db.session.add(usr)
            db.session.commit()
        else:
            if(found_user.pwd != password):
                flash("Incorrect password")
                return render_template("root.html")
        
        found_user = users.query.filter_by(user=user.lower()).first()

        session["user"] = user.lower()
        return redirect(url_for("profile", name=user))
    return render_template("root.html")

@app.route('/<name>', methods=['GET', 'POST'])
def profile(name):
    check=""
    status = 0
    if "user" not in session:
        status = 1
    elif session["user"] != name.lower():
        status = 2

    found_user = users.query.filter_by(user=name.lower()).first()

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
            #check = found_user.mbti = functions.detect(0)
        elif request.form.get("dnd"):
            return redirect(url_for("dndPg", name=name))
            # check = found_user.dnd = functions.detect(1)
        elif request.form.get("type"):
            return redirect(url_for("gramPg", name=name))
            # check = found_user.types = functions.detect(2)
            
        # if(check != "?"):
        #     db.session.commit()
        # else:
        #     flash("Something went wrong, please try again")
        #     db.session.rollback()

    # Errors pile up from arr without this, likely because the compiler has a possibility of checking a none-type
    arr = ["", "", "", "", "", ""]
    if(found_user is not None):
        arr = [name, found_user.mbti, found_user.dnd, found_user.types, "Logout", found_user.pwd]

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
        driverM = functions2.headless(0)
        try:
            check = functions2.mbtiSubmit(driverM, opinions)
        except:
            flash("Something went wrong, please try again")
            driverM.quit()
            return redirect(url_for("profile", name=session["user"]))

        driverM.quit()
        found_user = users.query.filter_by(user=name.lower()).first()
        found_user.mbti = check
        db.session.commit()
        flash("Your MBTI type is " + check)
        return redirect(url_for("profile", name=session["user"]))

    driver = functions2.headless(0)
    arr = functions2.mbtiScrape(driver)
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
        driverD = functions2.headless(1)
        try:
            check = functions2.dndSubmit(driverD, opinions)
        except:
            flash("Something went wrong, please try again")
            driverD.quit()
            return redirect(url_for("profile", name=session["user"]))
        
        driverD.quit()
        found_user = users.query.filter_by(user=name.lower()).first()
        found_user.dnd = check
        db.session.commit()
        flash("Your DND alignment is " + check)
        return redirect(url_for("profile", name=session["user"]))

    driver = functions2.headless(1)
    arr = functions2.dndScrape(driver)
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
            name = val[:val.find("--")]
            val = int(val[-1])
            opinions[0].append(name)
            opinions[1].append(val)
        # driver = functions2.headless(2)
        # print(functions2.gramSubmit(driver, opinions))
        # driver.quit()
        driverG = functions2.headless(2)
        try:
            check = functions2.gramSubmit(driverG, opinions)
        except:
            flash("Something went wrong, please try again")
            driverG.quit()
            return redirect(url_for("profile", name=session["user"]))
        
        driverG.quit()
        found_user = users.query.filter_by(user=name.lower()).first()
        found_user.types = check
        db.session.commit()
        flash("Your Enneagram type is " + check)
        return redirect(url_for("profile", name=session["user"]))
    
    driver = functions2.headless(2)
    arr = functions2.gramScrape(driver)
    driver.quit()
    j = 0
    for i in arr[0]:
        nums.append(j)
        j += 1    
    return render_template("gram.html", qs = arr, nums = nums)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)