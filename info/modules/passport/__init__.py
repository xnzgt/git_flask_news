# 创建蓝图接收前端发送数据
from flask import Blueprint
# 设置url_prefix用于与其他蓝图进行区分
passport_blu = Blueprint("passport",__name__,url_prefix="/passport")

from .views import *
