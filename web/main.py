from quart import Quart, render_template, jsonify

app = Quart(__name__)

@app.route('/')
async def hello():
    return await render_template('index.html')

@app.route('/list')
async def list():
    return str(['one','two','three'])

@app.route('/widget.js')
async def widget():
    return jsonify({'a':'widget'}) 

app.run('0.0.0.0',5002)
