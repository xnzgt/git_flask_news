# 创建新闻详情页路由
from flask import render_template

from info.modules.news import news_blu


@news_blu.route("/<int:news_id>")
def news_detail():
    return render_template("news/detail.html")