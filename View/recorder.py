from flask import Flask, render_template, request, make_response, send_file, Response, jsonify
from werkzeug import secure_filename
from flask_cors import CORS
from flaskext.mysql import MySQL
from flask_socketio import SocketIO
from flask_socketio import send, emit
import os
import sys
import cv2
import time
import glob
import pickle
import io
import math
import datetime


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = '/'
socketio = SocketIO(app)
fps = 3
done = False



@socketio.on('connect')
def test_connect():
    emit('my', {'data': 'Connected'})

@socketio.on('get')
def _get():
      files = [s for s in os.listdir('./recordings')
          if os.path.isfile(os.path.join('./recordings', s))]
      for i in range(len(files)):
            emit('postt', files[i])


def getNextFrame():
      files = [s for s in os.listdir('./frames')
          if os.path.isfile(os.path.join('./frames', s))]
      files.sort(key=lambda s: os.path.getmtime(os.path.join('./frames', s)))
      if len(files) > 0:
            nextFile = files[0]
            return ('./frames/' + nextFile)
      else:
            return None


@socketio.on('start')
def _start():
      global fps
      global done
      done = False
      out = cv2.VideoWriter('recordings/{date:%Y-%m-%d-%H-%M-%S}.webm'.format( date=datetime.datetime.now()),cv2.VideoWriter_fourcc(*'VP80'), fps, (640,480), True)
      f = getNextFrame()
      st = time.time()
      while True:
            if f is not None:
                  st = time.time()
                  frame = cv2.imread(f)
                  out.write(frame)
                  try:
                        os.remove(f)
                  except:
                        pass
                  
            try: 
                  f = getNextFrame()
            except:
                  pass
            
            if time.time()-st > 3 and done:
                  break


@app.route('/stop', methods = ['GET', 'POST'])
def ss_top():
      global done
      done = True
      return 'done'

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
      if request.method == 'POST':
            file = request.files['file']
            if file:
                  filename = secure_filename(file.filename)
                  file.save(os.path.join('frames', filename))
            return 'file uploaded successfully'

@app.route('/uploadVideo', methods = ['GET', 'POST'])
def uploadVid():
      global fps

      if request.method == 'POST':
            file = request.files['file']
            if file:
                  filename = secure_filename('vid')
                  file.save(filename)
            vidcap = cv2.VideoCapture('vid')
            fpsLoaded = vidcap.get(cv2.CAP_PROP_FPS)
            m=((fpsLoaded)/fps)
            cur = 0

            success,image = vidcap.read()
            height , width , layers =  image.shape
            out = cv2.VideoWriter('recordings/{date:%Y-%m-%d-%H-%M-%S}.webm'.format( date=datetime.datetime.now()),cv2.VideoWriter_fourcc(*'VP80'), fps, (width,height), True)
            success = True
            while success:
                  success,image = vidcap.read()
                  out.write(image)
                  cur+=m
                  cur = math.ceil(cur)
                  vidcap.set(1,cur)
                  if cur > 1 and vidcap.get(1) < 1:
                        break
            vidcap.release()
            out.release()
            return 'file uploaded successfully'

		
if __name__ == '__main__':
   files = [s for s in os.listdir('./frames')
          if os.path.isfile(os.path.join('./frames', s))]
   for i in range(len(files)):
         os.remove(os.path.join('./frames', files[i]))
   app.run(host='0.0.0.0', port=4125, threaded=True)
   socketio.run(app)
