import logging
from logging.handlers import RotatingFileHandler       #日志

from flask import Flask
from flask_sqlalchemy import SQLAlchemy        #数据库
from flask_wtf import CSRFProtect             #csrf保护
from flask_session import Session             #设置session保存位置
import redis
from config import config_dict        #导入配置文件字典

db = SQLAlchemy()          #获取数据库对象

redis_store = None

'''创建app的方法'''
def create_app(config_name):
    '''通过传入不同的配置名，切换不同的环境'''

    app = Flask(__name__)  # 获取app实例

    # 根据传进来的config_name以字典方式获取对应的类
    config = config_dict.get(config_name)
    # 关联config类中的配置
    app.config.from_object(config)
    # 根据config类中的LEVEL设置日志级别，由于继承父类Config，默认为DEBUG
    log_file(config.LEVEL)

    db.init_app(app)  # 数据库对象关联app

    # 初始化全局redis配置
    global redis_store
    redis_store = redis.StrictRedis(host=config.RDIES_HOST,port=config.RDIES_PORT,decode_responses=True)

    # 开启csrf保护，只用于服务器验 证
    # CSRFProtect(app)

    # 设置session保存位置
    Session(app)

    #在创建app时注册蓝图
    from newsInfo.modules.index import index_blue
    app.register_blueprint(index_blue)

    from newsInfo.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    #注册过滤器
    from newsInfo.utils.common import do_index_class
    app.add_template_filter(do_index_class,'index_class')

    return app



'''记录日志'''
def log_file(level):
    '''根据传进来的level进行操作'''
    # 设置日志的记录等级,常见等级有: DEBUG<INFO<WARING<ERROR
    logging.basicConfig(level=level)  # 调试debug级

    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)

    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')

    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)

    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)