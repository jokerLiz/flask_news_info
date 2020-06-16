from flask import Flask
from flask_sqlalchemy import SQLAlchemy        #数据库
from flask_wtf import CSRFProtect             #csrf保护
from flask_session import Session             #设置session保存位置
import redis
from config import Config        #导入配置文件

app = Flask(__name__)      #app实例

'''app设置'''
app.config.from_object(Config)          #关联app配置

db = SQLAlchemy(app)          #关联数据库

# 初始化redis配置
redis.StrictRedis(host=Config.RDIES_HOST,port=Config.RDIES_PORT)

# 开启csrf保护，只用于服务器验 证
CSRFProtect(app)

# 设置session保存位置
Session(app)

'''创建app的方法'''
def create_app(config):
    pass
