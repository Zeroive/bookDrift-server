from flask import Blueprint, request
import json
import requests
from tools.WXBizDataCrypt import WXBizDataCrypt
from app.user.models import USER
from tools.areaList import areaList

user = Blueprint('user', __name__, url_prefix="/user")
userService = USER()

appID = 'wx1f0a49be56df29ea'  # 开发者关于微信小程序的appID
appSecret = '3446adde90cbf3b283d6ab36d50ac1ec'  # 开发者关于微信小程序的appSecret


@user.route('/')
def index():
    return "hello user"


@user.route('/login', methods=['POST'])
def user_login():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    code = request_data['code']  # 前端POST过来的微信临时登录凭证code

    req_params = {
        'appid': appID,
        'secret': appSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'

    rawdata = requests.get(wx_login_api, params=req_params).json()  # 向API发起GET请求
    openid = rawdata['openid']  # 得到用户关于当前小程序的OpenID
    session_key = rawdata['session_key']  # 得到用户关于当前小程序的会话密钥session_key

    response_data = {
        'accessToken': '-'.join([openid, session_key])
    }

    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


@user.route('/getuserprofile', methods=['POST'])
def get_user_profile():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    response_data = {}
    temp = request_data['accessToken'].split('-')
    openid = temp[0]
    session_key = temp[1]
    encryptedData = request_data['encryptedData']
    iv = request_data['iv']

    pc = WXBizDataCrypt(appID, session_key)  # 对用户信息进行解密
    userinfo = pc.decrypt(encryptedData, iv)  # 获得用户信息

    if not userService.finduserbyopenid(openid):
        data = userinfo
        data['openId'] = openid
        data['sessionKey'] = session_key
        userService.insertOne(data)

    response_data['userinfo'] = userService.finduserbyopenid(openid)
    # print(response_data['userinfo'])

    # 处理背景图片
    img = requests.get(userinfo['avatarUrl']).content
    response_data['userinfo']['fontcolor'] = userService.judgeimage(img)
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


@user.route('/updateaddress', methods=['POST'])
def update_user_address():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    # print(request_data)
    areacode = int(request_data['id'])
    # 设置省市区
    request_data['province'] = areaList['province_list'][str(int(areacode/10000)*10000)]
    request_data['city'] = areaList['city_list'][str(int(areacode/100)*100)]
    request_data['district'] = request_data['fullname']
    request_data['latitude'] = request_data['location']['latitude']
    request_data['longitude'] = request_data['location']['longitude']
    userService.updatebyuserid(request_data, request_data['accessToken'].split('-')[0])
    response_data = {}
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)
