# 抽取app的创建逻辑
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config
from redis import StrictRedis


# TODO 2:Error 111 connecting to 127.0.0.1:6379. Connection refused.BUG是因为redis服务未启动


db = SQLAlchemy()
# 创建log日志
def set_log(config_name):
    # 通过不同配置创建不同的日志记录类型
    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].DEBUG) # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

redis_store = None # type:StrictRedis
# 可变参数，用函数封装或放在配置文件中
def create_app(config_name):
    set_log(config_name)
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 初始化数据库对象
    db.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST,port=config[config_name].REDIS_PORT,decode_responses=True)
    # 开启csrf
    # CSRFProtect(app)
    # 初始化Session
    Session(app)
    # TODO 3:只用一次的模块什么时候用什么时候导入
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)
    # 注册图片验证码蓝图
    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)
    return app