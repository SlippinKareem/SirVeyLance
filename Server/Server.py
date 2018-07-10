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
import hashlib



app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = '/'
socketio = SocketIO(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sir_vey_lance'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor =conn.cursor()
usr = ""
fps = 3
current = 'no'
last = [0] * 6




@socketio.on('connect')
def test_connect():
    emit('my', {'data': 'Connected'})

@socketio.on('getSettings')
def userSettings(msg):
    global usr
    cursor.execute("SELECT * from users where users.Name = '" + msg + "';")
    data = cursor.fetchone()
    usr = str(data[0])
    cursor.execute("SELECT * from user_settings where user_settings.userID = '" + str(data[0]) + "';")
    data = cursor.fetchall()
    for i in range(len(data)):
          
          emit('returnSettings', {'s': str(data[i][1]), 'e': str(data[i][2])})


@socketio.on('getStreamSummary')
def _getStreamSummary(msg):
    global usr
    cursor.execute("SELECT * from users where users.Name = '" + msg + "';")
    data = cursor.fetchone()
    usr = str(data[0])
    cursor.execute("SELECT * from surv_summary where surv_summary.userID = '" + str(data[0]) + "';")
    data = cursor.fetchall()
    for i in range(len(data)):
          rec = {
                'a': data[i][1],
                's': str(data[i][2]),
                'e': str(data[i][3]),
                'n': str(data[i][4])
          }
          emit('summary', rec)

@socketio.on('getStreamStats')
def _getStreamStats(msg):
    global usr
    cursor.execute("SELECT * from users where users.Name = '" + msg + "';")
    data = cursor.fetchone()
    usr = str(data[0])
    cursor.execute("SELECT surv_summary.actionID, COUNT(*) AS count FROM surv_summary WHERE surv_summary.userID = '" + str(data[0]) + "' GROUP BY surv_summary.actionID;")
    data = cursor.fetchall()
    
    for i in range(len(data)):
          rec = {
                'a': data[i][0],
                'n': data[i][1]
          }
          emit('stats', rec)


@socketio.on('changeUserName')
def _changeUserName(msg):
    global usr
    password = msg['pwd']
    salt = "sVl"
    password = password + salt
    password = hashlib.md5(password.encode()).hexdigest()

    cursor.execute("SELECT * from users where users.Name = '" + msg['old'] + "' and users.Token = '" + password + "';")
    data = cursor.fetchall()
    if len(data) == 0:
          emit('fail')
          return
    usr = str(data[0][0])
    cursor.execute("UPDATE users set Name = '" + msg['new'] + "' Where ID = " + usr + ";")
    conn.commit()
    emit('success')

@socketio.on('changePassword')
def _changePassword(msg):
    global usr
    password = msg['old']
    salt = "sVl"
    password = password + salt
    password = hashlib.md5(password.encode()).hexdigest()

    cursor.execute("SELECT * from users where users.Name = '" + msg['usr'] + "' and users.Token = '" + password + "';")
    data = cursor.fetchall()
    if len(data) == 0:
          emit('fail')
          return
    usr = str(data[0][0])
    password = msg['new']
    salt = "sVl"
    password = password + salt
    password = hashlib.md5(password.encode()).hexdigest()

    cursor.execute("UPDATE users set Token = '" + password + "' Where ID = " + usr + ";")
    conn.commit()
    emit('success')

@socketio.on('postUserAction')
def _postUserAction(msg):
    global usr
    cursor.execute("SELECT * from users where users.Name = '" + msg['user'] + "';")
    data = cursor.fetchone()
    usr = str(data[0])
    cursor.execute("CALL post_user_action(" + str(data[0]) + ", " + msg['action'] + ");")
    conn.commit()


@socketio.on('deleteUserAction')
def _deleteUserAction(msg):
    global usr
    cursor.execute("SELECT * from users where users.Name = '" + msg['user'] + "';")
    data = cursor.fetchone()
    usr = str(data[0])
    cursor.execute("CALL delete_user_action(" + str(data[0]) + ", " + msg['action'] + ");")
    conn.commit()


@socketio.on('parking')
def pp(msg):
    global usr
    cursor.execute("SELECT * from users where users.Name = '" + msg['user'] + "';")
    data = cursor.fetchone()
    usr = str(data[0])
    cursor.execute("UPDATE user_settings SET extra_info=" + str(msg['in']) + " WHERE userID=" + str(data[0]) +  " AND actionID=2;")
    conn.commit()


@socketio.on('crowd')
def cc(msg):
    global usr
    cursor.execute("SELECT * from users where users.Name = '" + msg['user'] + "';")
    data = cursor.fetchone()
    usr = str(data[0])
    cursor.execute("UPDATE user_settings SET extra_info=" + str(msg['in']) + " WHERE userID=" + str(data[0]) +  " AND actionID=3;")
    conn.commit()


@socketio.on('startRec')
def _startRec(msg):
    global current
    global last
    last = [0] * 6
    current = msg['gt']

@socketio.on('nn')
def _nn(msg):
    global current
    global last
    last = [0] * 6
    current = msg['gt']

def getNextFrame():
      files = [s for s in os.listdir('./frames')
          if os.path.isfile(os.path.join('./frames', s))]
      files.sort(key=lambda s: os.path.getmtime(os.path.join('./frames', s)))
      if len(files) > 0:
            nextFile = files[0]
            return ('./frames/' + nextFile)
      else:
            return None

@app.route('/getNxtFrame', methods = ['GET', 'POST'])
def GF():
   st = time.time()
   if request.method == 'GET':
      f = getNextFrame()
      if f is None:
            return Response("{'please move along':'nothing to see here'}", status=404, mimetype='application/json')
      with open(f, 'rb') as bites:
                    
        ret = send_file(
                     io.BytesIO(bites.read()),
                     attachment_filename='IMG.jpeg',
                     mimetype='image/jpg'
               )
      os.remove(f)
      if 'IMG0.jpeg' in f:
            return ret, 205
      return ret


@app.route('/settings', methods = ['GET', 'POST'])
def sett():
    global usr
    if request.method == 'GET':
      cursor.execute("SELECT * from user_settings where user_settings.userID = '" + usr + "';")
      data = cursor.fetchall()
      res = {
            '1': '0',
            '2': '0',
            '3': '0',
            '4': '0',
            '5': '0',
            '6': '0'
      }
      for i in range(len(data)):
            res[str(data[i][1])] = str(data[i][2])
      return jsonify(res)



@socketio.on('action_gded')
def on_action_gded(msg):
      global current
      global usr
      global last
      global fps
      if msg['e'] == 1:#start
            cursor.execute("CALL post_summary('"  + str(146) +"','"  + str(msg['a']) +"','"  + str(msg['s']/fps) +"','"  + str(0) +"','"  + current + "');")
            conn.commit()
            last[msg['a'] - 1] = msg['s']
            msg['s'] = msg['s']/fps
            emit('update', msg, broadcast=True, include_self=False)
      if msg['e'] == 2:#end
            cursor.execute("UPDATE `surv_summary` SET `end`=" + str(msg['s']/fps) +" WHERE `start`="+ str(last[msg['a'] - 1])+" and `userID`=" +usr +" and `actionID`=" +str(msg['a']) + " and `gt`='"+current +"';")
            conn.commit()
            last[msg['a'] - 1] = 0


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
   global usr
   if request.method == 'POST':
      result = request.form
      email = (result['email'])
      password = (result['password'])
      salt = "sVl"
      password = password + salt
      password = hashlib.md5(password.encode()).hexdigest()

      cursor.execute("SELECT * from users where users.Name = '" + email + "';")
      data = cursor.fetchall()
      if len(data) == 0: 
            cursor.execute("INSERT INTO `users`(`Name`, `Token`) VALUES ('" + email +"','" + password + "');")
            conn.commit()
            resp = make_response('')
            resp.set_cookie('name', email)
            resp.set_cookie('new', '1')
            cursor.execute("SELECT * from users where users.Name = '" + email + "';")
            data = cursor.fetchone()
            usr = str(data[0])
            return resp
      resp = make_response('')
      resp.set_cookie('name', '')
      return resp


@app.route('/login', methods = ['GET', 'POST'])
def login():
   global usr
   if request.method == 'POST':
      result = request.form
      email = (result['em'])
      password = (result['ps'])
      salt = "sVl"
      password = password + salt
      password = hashlib.md5(password.encode()).hexdigest()

      cursor.execute("SELECT * from users where users.Name = '" + email + "';")
      data = cursor.fetchall()
      if len(data) == 1 and data[0][2] == password: 
            usr = str(data[0][0])
            resp = make_response('')
            resp.set_cookie('name', email)
            resp.set_cookie('new', '0')
            return resp
      resp = make_response('')
      resp.set_cookie('name', '')
      return resp

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
            count = 0
            success = True
            while success:
                  success,image = vidcap.read()
                  cv2.imwrite("frames/IMG%d.jpeg" % count, image)     # save frame as JPEG file
                  cur+=m
                  cur = math.ceil(cur)
                  vidcap.set(1,cur)
                  if cur > 1 and vidcap.get(1) < 1:
                        emit('fail', broadcast=True)
                        break
                  count += 1
            vidcap.release()
            return 'file uploaded successfully'

@app.route('/', methods = ['GET', 'POST'])
def index():
      return 'Connected'
		
if __name__ == '__main__':
   f = getNextFrame()
   files = [s for s in os.listdir('./frames')
          if os.path.isfile(os.path.join('./frames', s))]
   for i in range(len(files)):
         os.remove(os.path.join('./frames', files[i]))
   app.run(host='0.0.0.0', port=6869, threaded=True)
   socketio.run(app)
