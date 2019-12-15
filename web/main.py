from quart import Quart, render_template, jsonify
import os 

import hardware

def vue_comp(path):
    l = os.listdir(path)
    t = "" 
    for i in l:
        if i.endswith('.vue'):
            print(i)
            data = open(path+os.sep+i).read()
            t += data
            t += '\n'
    return t

vc = vue_comp('templates/vuecomp')

app = Quart(__name__)
bf = hardware.BoardFinder()

@app.route('/')
async def hello():
    return await render_template('index.html')

@app.route('/list')
async def list_boards():
    val  = list(hardware.list_boards().keys())
#    val = bf.resources()
    print(val)
    return jsonify(val)

@app.route('/widget.js')
async def widget():
    return vc

app.run('0.0.0.0',5002)
