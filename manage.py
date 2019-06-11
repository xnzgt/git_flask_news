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
# 集成flask设置数据库迁移扩展
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from config import Config
from info import create_app,db,models


app = create_app("develop")
# 初始化manager对象
manager = Manager(app)
# TODO:Migrate位置问题
Migrate(app,db)
manager.add_command('db',MigrateCommand)




if __name__ == '__main__':
    # app.run()
    # print(app.url_map)
    # TODO 4:数据库迁移使用manager运行
    manager.run()