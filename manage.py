from flask import Flask
# 2:配置数据库
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1:集成配置类
class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1/git_flask_news"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(Config)

db = SQLAlchemy(app)


@app.route('/')
def index():
    return "helloWorld"

if __name__ == '__main__':
    app.run(debug=True)