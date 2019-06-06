from flask import Flask, session
# 2:配置数据库
from flask_sqlalchemy import SQLAlchemy
# 3:集成redis
import redis
# 4:设置csrf验证
from flask_wtf import CSRFProtect
# 5:将session保存到Session中
from flask_session import Session
from redis import StrictRedis

app = Flask(__name__)

# 1:集成配置类
class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1/git_flask_news"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 配置flask_session四项参数
    # 指定session存储方式
    SESSION_TYPE = "redis"
    # 指定储存session的储存对象
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    # 设置session签名
    SESSION_USR_SIGNER = True
    # 设置session不永久保存
    SESSION_PERMANENT = False
    # 设置session保存时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2

app.config.from_object(Config)
# 初始化数据库对象
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 开启csrf
CSRFProtect(app)
# 初始化Session
Session(app)

@app.route('/')
def index():
    # 测试session
    session["name"] = "谢年智"
    return "helloWorld"

if __name__ == '__main__':
    app.run(debug=True)