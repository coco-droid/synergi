from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from agent.synergi import SynergiAgent

app = Flask(__name__)
socketio = SocketIO(app)
synergi = SynergiAgent()

@socketio.on('connect')
def on_connect():
    print('Client connected')
    
@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@socketio.on('message') 
def handle_message(msg):
    print(msg)
    response = synergi.handle_message(msg)
    emit('message', {'message': response})

@app.route('/api', methods=['POST'])  
def api_message():
    content = request.get_json()
    # Do something
    
    socketio.emit('message', content) 
    return {'status': 'success'}

@app.route('/')
def index():
    return 'Hello, World!'
    
if __name__ == "__main__":
    socketio.run(app)