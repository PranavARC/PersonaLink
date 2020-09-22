from flask import Flask, request, redirect, url_for, render_template, session
from datetime import timedelta
import functions

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=3)

@app.route('/', methods=['GET', 'POST'])
def main():
    if "user" in session:
        return redirect(url_for("profile"))    
    if request.method == 'POST':
        session.permanent = True
        user = request.form["username"]
        password = request.form["password"]
        session["user"] = user
        session["password"] = password
        session["mbti"] = "?"
        session["dnd"] = "?"
        session["types"] = "?"
        return redirect(url_for("profile"))
    else:
        return render_template("root.html")

@app.route('/my-profile', methods=['GET', 'POST'])
def profile():
    arr = ["","","","",""]
    if "user" in session:
        arr = [session["user"], session["password"], session["mbti"], session["dnd"], session["types"]]
    if request.method == 'POST':
        if request.form.get("mbti"):
            session["mbti"] = arr[2] = functions.detect(0) 
        elif request.form.get("dnd"):
            session["dnd"] = arr[3] = functions.detect(1)
        elif request.form.get("type"):
            session["types"] = arr[4] = functions.detect(2)
    return render_template("profile.html", arr = arr)

# @app.route("/<name>")
# def rando(name):
#     return f"Hello {name}!"

if __name__ == "__main__":
    app.run(debug=True)