# 抽取app的创建逻辑
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# 初始化数据库对象
db = SQLAlchemy(app)

redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 开启csrf
CSRFProtect(app)
# 初始化Session
Session(app)