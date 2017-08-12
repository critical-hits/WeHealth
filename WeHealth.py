# -*- coding: utf-8 -*-
import sqlite3
import requests
from flask import Flask, render_template, g, request
from Connect import sendData
app = Flask(__name__)
DATABASE = 'myhealth.db'
"""
响应请求
"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/block')
def block():
    blocks=[]
    for data in query_db('select * from users'):
        print user['username'], 'has the id', user['user_id']
        blocks.append({id:data['id'],msg:data['msg'],cost:data['cost'],\
                      hash:data['hash'],time:data['time']})

    return render_template('block.html',blocks=blocks)


@app.route('/addBlock', methods=['POST', 'GET'])
def addBlock():
    data=request.form['id']+":"+request.form['cost']\
                    +":"+request.form['msg']
    sendData(data,'192.168.43.116')
    return 'success'


@app.route('/status')
def status():
    return render_template('status.html')


def init_db():
    with app.app_context():
        db = get_db()
        createTable = "create table if not exists block " \
                      "(id varchar(20) primary key, " \
                      "money int(10), " \
                      "description varchar(20), " \
                      "hashValue varchar(500))"
        with app.open_resource(createTable, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# @app.route('/nodes')
# def nodes():
#     return render_template('nodes.html')
def post_msg():
    pass


'''
数据库连接
'''
def connect_db():
    return sqlite3.connect(DATABASE)

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
'''
测试页面
1.容灾
2.篡改
3.输入
'''


@app.route('/input')
# 测试输入一个node和一个信息
def input():
    return 'input'


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
