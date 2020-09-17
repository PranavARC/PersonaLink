from flask import Flask, request
import functions

app = Flask(__name__)

bro = "idk"
stuff = ""

webstring = """Let's begin \n <h1> """ + bro + """ 
hey <h1>
<form method="POST" action="send">
    <input class="button" type="submit" value="submit">
</form> """

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        stuff = functions.detect(0)
        
    return "Here is your type: " + stuff

@app.route("/")
def bruh():
    return webstring

@app.route("/<name>")
def rando(name):
    return f"Hello {name}!"


if __name__ == "__main__":
    app.run()