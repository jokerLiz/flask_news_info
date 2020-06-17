#视图
from flask import render_template

from . import index_blue      #导入__init__.py下的蓝图对象index_blue


#为该蓝图编写视图函数
@index_blue.route('/')
def index():
    return render_template('news/index.html')