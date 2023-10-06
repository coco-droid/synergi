from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from agent.synergi import SynergiAgent
from agent.contextual import ContextConversation
from others.og import OpenGraphScraper
from werkzeug.utils import secure_filename
import time
import json
import os
from queued.queued import  QueueManager
#launch redis-server  in another console

print("redis is launch")
app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')
redis_url = 'redis://localhost:6379/0'  # URL de votre instance Redis
queue_manager = QueueManager(redis_url)
synergi = SynergiAgent()
#store emit in a global variable 
@socketio.on('connect')
def on_connect():
  print('Client connected')
@socketio.on('disconnect')
def on_disconnect():
  print('Client disconnected')

@socketio.on('message')
def handle_message(msg):
  try:
    print(f"Received message: {msg}")
    txt = msg['sendMessage']
    response = synergi.handle_message(txt,emit)
  except Exception as e:
    print(f"Error: {e}")
    response = "Désolé, une erreur s'est produite lors du traitement de votre requête."

  #emit('message', {'message': response})
@socketio.on('delete_history')
def delete_history(msg):
  print(f"Received : {msg}")
  response = ContextConversation()
  res=response.delete_date_conversation_on_redis(msg['date'])
  emit('history_deleted', {'message': 'deleted'})
@socketio.on('get_history')
def get_history(msg):
  print(f"Received message: {msg}")
  if msg['req']=="date":
    response = ContextConversation()
    res=response.get_conversation_dates() 
    emit('history', {'message': res})  
  else:
    response = ContextConversation()
    res=response.get_conversation(msg['date'])
    emit('history', {'message': res})
@socketio.on('with_file')
async def on_file(data):
  print(f"Received file: {data['name']}")
  file_path = os.path.join('./uploads', data['name'])
  with open(file_path, 'wb') as f:
    await f.write(data['data'])
  print(f"File saved: {file_path}") 
@socketio.on('opengraph')
def read_scrape(urls):
    urls=urls['url']
    print(urls)
    response={}
    #loop through urls
    for url in urls:
      scraper = OpenGraphScraper(url)
      og_data = scraper.get_opengraph_data()
      response[url]=og_data
    print('Trace:')
    print(response)
    # detect if the response object is empty
    if  bool(response):
       emit('opengraph_data',response)

UPLOAD_FOLDER = 'uploads'
app.config[''] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    file_path = os.path.join('static', filename)
    file.save(file_path)
    file_url = file_path  # Replace with your domain and path
    return json.dumps({'success': True, 'file': {'url': file_url}})


@app.route('/message', methods=['POST'])
def user_message():
   print('lol me')
   request_data = request.get_json()
   print(request_data)
   try:
    if (request_data['haveFile']):
        print(f"Received message: {request_data['sendMessage']} with file:{request_data['name']} ")
        txt = request_data['sendMessage']
        print(request)
        response = synergi.handle_message_with_files(txt,request_data['name'].replace(" ", "_"))
    else:
        print(f"Received message: {request_data['sendMessage']}")
        txt = request_data['sendMessage']
        print(request)
        response = synergi.handle_message(txt,emit)
   except Exception as e:
    print(f"Error me this: {e}")
    response=e
    #response = "Désolé, une erreur s'est produite lors du traitement de votre requête."
   return {'msg':response}
@app.route('/api', methods=['POST'])  
def api_message():
  content = request.get_json()
  # Do something
  
  socketio.emit('message', content) 
  return {'status': 'success'}

@app.route('/')
def index():
  return 'Hello, World!'
  
def emit_queued_messages():
    while True:
        messages = queue_manager.get_messages()
        for message in messages:
            event = message['event']
            data = message['message']
            socketio.emit(event, data)
        time.sleep(1)  # Émettez des événements chaque seconde

if __name__ == '__main__':
    socketio.start_background_task(emit_queued_messages)
    socketio.run(app, host='localhost', port=5000,debug=True,use_reloader=True)#loop = asyncio.get_event_loop() host='0.0.0.0'
   #loop.run_until_complete(socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=True))

