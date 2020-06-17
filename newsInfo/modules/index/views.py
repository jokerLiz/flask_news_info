#视图
from flask import render_template, current_app

from . import index_blue      #导入__init__.py下的蓝图对象index_blue


'''为该蓝图编写视图函数'''
#首页
@index_blue.route('/')
def index():
    return render_template('news/index.html')

#网页标签logo
@index_blue.route('/favicon.ico')
def get_web_logo():
    return current_app.send_static_file('news/favicon.ico')