from flask import request, abort, current_app, make_response

from info import redis_store, constants
from info.modules.passport import passport_blu

# 定义接收前端数据的视图函数
from info.utils.captcha.captcha import captcha


@passport_blu.route("/image_code")
def get_img_code():
    """
    生成图片验证码并返回
    :return:
    """
    # 1：取到参数
    image_code_id = request.args.get("imageCodeId",None)
    # 2：判断参数是否为空
    if not image_code_id:
        return abort(403)
    # 3：从工具包中生成图片验证码,返回值是元组
    name,text,image = captcha.generate_captcha()

    # 4：将图片验证码保存到redis中
    try:
        redis_store.setex("ImageCodeId:" + image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger(e)
        abort(500)
    # 5：返回验证码图片到前端
    response = make_response(image)
    # 设置响应数据类型
    response.headers['Content-Type'] = "image/jpg"
    return response