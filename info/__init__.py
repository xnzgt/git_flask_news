# 抽取app的创建逻辑
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config

app = Flask(__name__)
def create_app(config_name):
    app.config.from_object(config[config_name])
    # 初始化数据库对象
    db = SQLAlchemy(app)

    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST,port=config[config_name].REDIS_PORT)
    # 开启csrf
    CSRFProtect(app)
    # 初始化Session
    Session(app)
    return app