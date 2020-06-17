#创建蓝图

from flask import Blueprint

#创建蓝图
index_blue = Blueprint('index',__name__)

#导入本包下的views
from . import views