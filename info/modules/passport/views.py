import random
import re
from flask import request, abort, current_app, make_response, jsonify

from info import redis_store, constants
from info.libs.yuntongxun.sms import CCP
from info.modules.passport import passport_blu
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET





# 发送短信后端实现
@passport_blu.route("/sms_code",methods=["POST"])
def send_sms_code():
    """
    # 接收前端发送的手机号，图片验证码，uuid
    # 校验三个值是否都存在
    # 校验手机号,正则
    # 检查图片验证码是否正确,与redis中保存的验证码比较正确
    # 定义随机验证码,用于向容联云发送
    # 向容联云发送生成验证码
    # 将验证码保存到redis中
    # 如果发送成功返回给前端提示
    """
    # 传入格式是json,需转换为字典格式
    return jsonify(errno=RET.OK, errmsg="短信发送成功")
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

    # 定义随机验证码
    sms_code_str = "%06d" % random.randint(0, 999999)
    # 将验证码保存到log日志中
    current_app.logger("短信验证码为:%d" % sms_code_str)
    # # 像容联云发送数据,数据发送失败提示报错误
    # result = CCP().send_template_sms(mobile, [sms_code_str, constants.SMS_CODE_REDIS_EXPIRES], 1)
    # if result != 0:
    #     return jsonify(errno=RET.DATAERR, errmsg="数据发送失败")

    # 将验证码保存到redis
    try:
        redis_store.setex("SMS_" + mobile, constants.SMS_CODE_REDIS_EXPIRES,sms_code_str)
    except Exception as e:
        current_app.logger(e)
        return jsonify(errno=RET.DBERR,errmsg="短信验证码保存错误")


    # 向前端发送信息提示短信发送成功
    return jsonify(errno=RET.OK, errmsg="短信发送成功")


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
    print(text)

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