from flask import Flask, request, redirect, url_for, render_template
import functions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def bruh():
    if request.method == 'POST':
        user = request.form["username"]
        password = request.form["password"]
        return redirect(url_for("send", mbti = "?", dnd = "?", types = "?", usr = user, word = password))
    else:
        return render_template("root.html")

@app.route('/login-<usr>-<word>-<mbti>-<dnd>-<types>', methods=['GET', 'POST'])
def send(mbti, dnd, types, usr, word):
    mb = mbti
    dn = dnd
    typ = types
    if request.method == 'POST':
        mb = functions.detect(0)
    return render_template("login.html", mbti = mb, dnd = dn, type = typ, usr = usr, word = word)

# @app.route("/<name>")
# def rando(name):
#     return f"Hello {name}!"

if __name__ == "__main__":
    app.run(debug=True)