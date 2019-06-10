from flask import render_template, current_app, session, jsonify

from info import redis_store
from info.models import User
from info.modules.index import index_blu
from info.utils.response_code import RET


@index_blu.route('/')
def index():
    # 设置首页右上角用户名显示
    """
    使用session中的user_id来判断用户是否登录
    :return:
    """
    user_id = session.get("user_id")
    user = None
    if user_id:
        try:
            user = User().query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR,errmsg="数据库查询错误")

    # 将列表中的数据库对象转换为字典
    user = user.to_dict() if user else None
    data = {
        "user_info":user
    }

    return render_template("news/index.html",data = data)

@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')