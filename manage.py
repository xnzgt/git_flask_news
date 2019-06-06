from flask import Flask
# 2:配置数据库
from flask_sqlalchemy import SQLAlchemy
# 3:集成redis
import redis

app = Flask(__name__)

# 1:集成配置类
class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1/git_flask_news"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

app.config.from_object(Config)
# 初始化数据库对象
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

@app.route('/')
def index():
    # 测试redis

    return "helloWorld"

if __name__ == '__main__':
    app.run(debug=True)