# -*- coding: utf-8 -*-
import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/block')
def block():
    return 'block'


@app.route('/status')
def status():
    return 'status'


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
    app.run()
