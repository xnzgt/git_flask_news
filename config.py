# 配置类代码抽取
# 1:集成配置类
from redis import StrictRedis


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