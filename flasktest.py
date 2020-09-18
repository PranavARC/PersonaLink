from flask import Flask, request, redirect, url_for, render_template
import functions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def bruh():
    if request.method == 'POST':
        user = request.form["username"]
        password = request.form["password"]
        return redirect(url_for("send", usr = user, word = password))
    else:
        return render_template("root.html")

@app.route('/login-<usr>-<word>')
def send(usr, word):
    return render_template("login.html", usr = usr, word = word)

@app.route("/<name>")
def rando(name):
    return f"Hello {name}!"


if __name__ == "__main__":
    app.run(debug=True)