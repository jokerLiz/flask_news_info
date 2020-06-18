from . import passport_blue

from flask import request, jsonify, current_app, make_response, json
from newsInfo.utils.response_code import RET             #返回 response响应使用的模板
from newsInfo.utils.captcha.captcha import captcha         #导入图片验证码工具包
from ... import redis_store, constants

import random
import re
from newsInfo.libs.yuntongxun.sms import CCP       #导入云通讯依赖包中的CCP


'''图片验证码'''
#功能描述: 图片验证码
#请求地址: /passport/image_code?cur_id=xxx&pre_id=xxx
#请求方式: GET
#请求参数: 随机字符串(uuid)cur_id, 上一个字符串:pre_id
#返回值:  返回图片
@passport_blue.route('/image_code')
def get_image_code():
    '''
    思路:
    1.获取参数
    2.校验参数，查看参数的存在性
    3.利用captcha工具获取验证码信息
    4.保存到redis中
    5.返回验证码图片信息
    :return:
    '''
    #1.获取url中?后的参数，也就是get方式访问携带的参数
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')

    #2.校验参数
    if not cur_id:
        return jsonify(errno = RET.PARAMERR,errmsg='参数不全')
    #3.生成图片验证码
    try:
        #获取图片信息
        name,text,image_data = captcha.generate_captcha()

        #保存到redis中
        '''
        参数1：保存到redis的key---图片id
        参数2：key对应的value-- 图片验证码的text文本
        参数3：过期时间
        '''
        redis_store.set('image_code:%s'%cur_id,text,constants.IMAGE_CODE_REDIS_EXPIRES)

        #判断有没有上一个图片的编号
        if pre_id:
            #释放该编号的验证码信息
            redis_store.delete('image_code:%s'%pre_id)
    except Exception as e:

        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg='验证码操作失败')

    #返回验证码图片信息
    response = make_response(image_data)   #16进制信息
    #把回应头改为image格式
    response.headers['Content-Type'] = 'image/jpg'

    return response




'''短信验证码'''
# 功能描述：发送短信
# 请求路径：/passport/sms_code
# 请求方式： POST
# 请求参数：mobile，image_code,image_code_id
# 参数格式：Json
# 返回值：errno,errmsg
@passport_blue.route('/sms_code',methods=['POST'])
def get_sms_code():
    '''
    思路分析：
    1. 获取参数
    2.校验参数，为空校验和格式校验
    3.取出redis中的图片验证码
    4.判断图片验证码是否过期
    5.如果过期，删除该验证码信息
    6.图片验证码的正确性判断
    7.生成短信验证码
    8.发送短信
    9.判断是否发送成功
    10.保存短信验证码到redis
    11.返回响应
    :return:
    '''
    #1. 获取参数
    json_data = request.data
    dict_data = json.loads(json_data)   #将json格式转化为字典
    mobile = dict_data.get('mobile')      #获取前端传来的三个参数
    image_code = dict_data.get('image_code')
    image_code_id = dict_data.get('image_code_id')

    # 2.校验参数
    if not all([mobile,image_code,image_code_id]):      #如果参数不全
        return jsonify(errno=RET.PARAMERR,errmsg='参数不足')

    if not re.match('1[3579]\d{9}',mobile):    #如果手机号码不合法
        return jsonify(errno=RET.PARAMERR,errmsg='手机格式不正确')

    # 3.取出redis中的图片验证码信息
    try:
        redis_image_code = redis_store.get('image_code:%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据获取失败')


    # 4.判断上一步获取的图片验证码信息是否过期
    if not redis_image_code:
        return jsonify(errno=RET.NODATA, errmsg="图片验证码过期")

    # 5.如果过期，删除redis中图片验证码
    try:
        redis_store.delete('image_code:%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="删除验证码失败")


    # 6.图片验证码正确性判断
    if image_code.upper() != redis_image_code.upper():
        return jsonify(errno=RET.DATAERR,errmsg='图片验证码错误')

    # 7.生成验证码
    sms_code = '%06d'%random.randint(0,999999)
    current_app.logger.debug(f'短信验证码：{sms_code}')

    # 8.发送验证码短信
    try:
        ccp = CCP()
        # 注意： 测试的短信模板编号为1
        # 参数1: 发送给谁的手机号
        # 参数2: ['内容', 有效时间单位分钟]
        # 参数3: 模板编号1  【云通讯】您使用的是云通讯短信模板，您的验证码是{1}，请于{2}分钟内正确输入

        result = ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="云通讯发送失败")

    # 9.判断验证码发送成功
    if result == -1:
        return jsonify(errno=RET.DATAERR , errmsg="发送短信失败")


    # 10.保存验证码到redis
    try:
        redis_store.set('sms_code:%s'%mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="短信保存失败")

    # 11.返回响应
    return jsonify(errno=RET.OK,errmsg='发送成功')
