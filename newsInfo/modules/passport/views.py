from . import passport_blue

from flask import request, jsonify, current_app, make_response
from newsInfo.utils.response_code import RET
from newsInfo.utils.captcha.captcha import captcha
from ... import redis_store, constants


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
        参数1：保存到redis的key
        参数2：图片验证码的text文本
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
