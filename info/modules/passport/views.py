import random
import re
from flask import request, abort, current_app, make_response, jsonify

from info import redis_store, constants
from info.libs.yuntongxun.sms import CCP
from info.modules.passport import passport_blu


from info.utils.captcha.captcha import captcha


# 发送短信后端实现
from info.utils.response_code import RET


@passport_blu.route("/",methods=["POST"])
def send_sms_code():
    """
    # 接收前端发送的手机号，图片验证码，uuid
    # 校验三个值是否都存在
    # 校验手机号,正则
    # 检查图片验证码是否正确,与redis中保存的验证码比较正确
    # 定义随机验证码,用于向容联云发送
    # 向容联云发送生成验证码
    # 如果发送成功返回给前端提示
    """
    # 传入格式是json,需转换为字典格式
    params_dict = request.json()
    # 接收三个数据 mobile,image_code,image_code_id
    mobile = params_dict.get("mobile")
    image_code = params_dict.get("image_code")
    image_code_id = params_dict.get("image_code_id")
    # 判断三个值是否都存在
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断手机号书写是否正确
    if not re.match(r"1[35678]\\d{9}", mobile):
        return jsonify(errno=RET.DATAERR, errmsg="手机号格式不正确")

    # 从redis中取出真实的图片验证码
    real_image_id = redis_store.get("ImageCodeId:" + image_code_id)
    # 与用户输入的图片验证码进行比较,不正确则提示
    if image_code_id.upper() != image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg="验证码输入错误")



# 定义接收前端图片验证码的视图函数
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