from quart import Quart, render_template, jsonify
import os 
def vue_comp(path):
    l = os.listdir(path)
    t = "" 
    for i in l:
        print(i)
        render_template(path+os.sep+i)
        data = ''
        t += data
        t += '\n'
    return t

vc = vue_comp('templates/vuecomp')
print(vc)

app = Quart(__name__)

@app.route('/')
async def hello():
    return await render_template('index.html')

@app.route('/list')
async def list():
    return str(['one','two','three'])

@app.route('/widget.js')
async def widget():
    return vc

app.run('0.0.0.0',5002)
