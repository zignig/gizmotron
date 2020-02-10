from quart import Quart, render_template, jsonify, session
import os
import uuid
import hardware


def vue_comp(path):
    l = os.listdir(path)
    t = ""
    for i in l:
        if i.endswith(".vue"):
            print(i)
            data = open(path + os.sep + i).read()
            t += data
            t += "\n"
    return t


vc = vue_comp("templates/vuecomp")

app = Quart(__name__)
app.secret_key = "notsosecret"
bf = hardware.BoardFinder()


@app.route("/")
async def hello():
    if "uuid" in session:
        value = session["uuid"]
    else:
        print("new session")
        value = uuid.uuid4()
        session["uuid"] = value
    print(value)
    return await render_template("index.html")


@app.route("/list.json")
async def list_boards():
    val = bf.list_boards()
    return jsonify(val)


@app.route("/widget.js")
async def widget():
    return vc


app.run("0.0.0.0", 5002)
