# -*- coding: utf-8 -*-
import sqlite3
import requests
import socket
from flask import Flask, render_template, g, request,jsonify
from Connect import sendData
app = Flask(__name__)
DATABASE = 'wehealth.db'
PORT = 5002
Node=['00','00','00','00','00','00','00','00']
import threading
"""
响应请求
"""
@app.route('/')
def index():
    blocks=[]
    for data in query_db('select * from block limit 5'):
        blocks.append({'id':data['id'],'msg':data['description'],'cost':data['money'],\
                      'hash':data['hashValue'],'time':data['time']})

    a=[]
    for i in range(0,7):
        a.append((Node[i])[1])
    return render_template('index.html',blocks=blocks,node=a)


@app.route('/block')
def block():
    blocks=[]
    for data in query_db('select * from block'):
        blocks.append({'id':data['id'],'msg':data['description'],'cost':data['money'],\
                      'hash':data['hashValue'],'time':data['time']})
    return render_template('block.html',blocks=blocks)


@app.route('/addBlock', methods=['POST', 'GET'])
def addBlock():
    data=request.form['id']+":"+request.form['cost']\
                    +":"+request.form['msg']
    sendData(data,'192.168.43.116')
    return 'success'

@app.route('/updateBlock', methods=['POST', 'GET'])
def updateBlock():
    updateSql='UPDATE block SET money=%s, description=%s\
            WHERE id=%s;'%(request.form['cost'],request.form['msg'],request.form['id'])
    db=get_connection()
    db.cursor().execute(updateSql)
    db.commit()
    return 'success'

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/getStatus', methods=['POST', 'GET'])
def getStatus():
    return jsonify(result=Node)


"""
数据库连接
"""

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_first_request
def before_first_request():
    lst  = Listener()   # create a listen thread
    lst.start() # then start

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

def init_db():
    with app.app_context():
        db = get_connection()
        createTable = "create table if not exists block " \
                      "(id varchar(20) primary key, " \
                      "money int(10), " \
                      "description varchar(20), " \
                      "hashValue varchar(500))"
        with app.open_resource(createTable, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

'''
测试页面
1.容灾
2.篡改
3.输入
'''
class Listener(threading.Thread):
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", PORT))
        sock.listen(0)
        while True:
            client, cltadd = sock.accept()
            print 'Connected by ', cltadd
            data = client.recv(1024)
            sp=data.split('#')
            print sp
            Node[int(sp[1])]=sp[0]
        sock.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
