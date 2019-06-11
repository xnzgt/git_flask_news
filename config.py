# 配置类代码抽取
# 1:集成配置类
import logging

from redis import StrictRedis


class Config(object):
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
    # 设置cookie的存活时间为浏览器结束,如果为true则跟session保存时间一致
    SESSION_PERMANENT = False
    # 设置session保存时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2


    # 设置日志等级
    LOG_LEVEL = logging.DEBUG
# 将相同的配置作为基类，其余的继承基类
# 开发环境类
class DevelopConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

# 生产环境类
class ProductConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.ERROR

# 测试环境类
class TestingConfig(Config):
    DEBUG = True


# 使用字典封装
config = {
    "develop":DevelopConfig,
    "product":ProductConfig,
    "testing":TestingConfig
}