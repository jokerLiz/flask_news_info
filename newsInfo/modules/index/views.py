#视图
from flask import render_template, current_app, session

from . import index_blue      #导入__init__.py下的蓝图对象index_blue

#网页标签logo
from ...models import User          #用户表


@index_blue.route('/favicon.ico')
def get_web_logo():
    return current_app.send_static_file('news/favicon.ico')

#首页
@index_blue.route('/')
def index():
    '''首页显示'''

    #通过session获取当前的用户id
    user_id = session.get('user_id')

    user = None
    #通过id查询用户的信息
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    data = {
        "user_info": user.to_dict() if user else None,     #to_dict():将对象中的信息转换为字典类型
    }

    return render_template('news/index.html',data=data)


