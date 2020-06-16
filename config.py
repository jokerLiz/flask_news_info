import os
import redis

#配置类
class Config(object):
    DEBUG = True

    #设置SECRET_KEY
    key = os.urandom(24)       #随机字符串
    SECRET_KEY = key


    '''mysql数据库设置'''
    host = 'localhost'
    port = '3306'
    useranme = 'root'
    password = 'root'
    db = 'information1'

    mysqlpath = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(useranme, password, host, port, db)
    SQLALCHEMY_DATABASE_URI = mysqlpath

    #数据库相关配置
    # 设置每次请求后自动提交数据库的改动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 动态追踪设置
    SQLALCHEMY_TRACK_MODUFICATIONS = True
    # 显示原始sql
    SQLALCHEMY_ECHO = True



    '''redis数据库设置'''
    RDIES_HOST = '127.0.0.1'
    RDIES_PORT = 6379

    '''flask session配置信息'''
    SESSION_TYPE = 'redis'       #指定session保存到redis数据库中
    SESSION_USE_SIGNER = True    #让cookie中的session被加密处理
    SESSION_REDIS = redis.StrictRedis(host=RDIES_HOST,port=RDIES_PORT)     #使用指定的redis的实例
    SESSION_PERMANENT = False      #过期时间
    PERMANENT_SESSION_LIFETIME = 86400    #session有效期


'''环境切换类'''
#开发环境
class DevelopConfig(Config):
    pass

#测试环境
class TestingConfig(Config):
    TESTING = True

#生产环境
class ProductConfig(Config):
    DEBUG = True

#这三个类通过统一的字典进行配置类访问
config_dict = {
    'develop':DevelopConfig,
    'testing':TestingConfig,
    'product':ProductConfig,

}