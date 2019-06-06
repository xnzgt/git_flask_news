# 抽取app的创建逻辑
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config
from redis import StrictRedis

# TODO 2:Error 111 connecting to 127.0.0.1:6379. Connection refused.BUG是因为redis服务未启动
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 初始化数据库对象
    db.init_app(app)

    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST,port=config[config_name].REDIS_PORT)
    # 开启csrf
    CSRFProtect(app)
    # 初始化Session
    Session(app)
    return app