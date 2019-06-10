from flask import render_template, current_app, session, jsonify

from info import redis_store, constants
from info.models import User, News, Category
from info.modules.index import index_blu
from info.utils.response_code import RET


@index_blu.route('/')
def index():
    # 新闻分类设置
    """
    从数据库中查出分类名
    添加进data字典中
    :return:
    """
    news_cly = Category.query.all()
    news_cly_list = [cly_name.to_dict() for cly_name in news_cly]
    print(news_cly_list)


    # 排行榜设计
    """
    从数据库中查出排行前六的列表
    将列表对象转化为字典
    发送给前端展示
    :return:
    """
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据库查询排行失败")
    news_hot = [news.to_basic_dict() for news in news_list]
    print("新闻排行:%s" % news_hot)


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

    # 定义字典向前端模板发送
    data = {
        "user_info":user,
        "news_hot":news_hot,
        "news_cly_list":news_cly_list
    }

    return render_template("news/index.html",data = data)

@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')