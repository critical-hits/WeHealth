# -*- coding: utf-8 -*-
import requests
from flask import Flask, render_template, g

app = Flask(__name__)

"""
响应请求
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/block')
def block():
    return render_template('block.html')

@app.route('/status')
def status():
    return 'status'

'''
数据库连接
'''
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_db():
    pass

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
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
    app.run(debug=True)
