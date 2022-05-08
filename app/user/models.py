from tools.db import DB
from PIL import Image, ImageStat
from io import BytesIO
import time


class USER(DB):

    def finduserbyopenid(self, openid):
        sql = 'SELECT * FROM user_info WHERE openId = "{}"'.format(openid)
        return self.select_one(sql)

    def insertOne(self, data):
        sql = 'INSERT INTO user_info(openId, sessionKey, nickName, avatarUrl, city, gender, province, ' \
              'country, language) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.\
            format(data['openId'], data['sessionKey'], data['nickName'], data['avatarUrl'], data['city'],
                   data['gender'], data['province'], data['country'], data['language'])
        self.inser_update_delete(sql)

    def updatebyuserid(self, map, openid):
        sql = 'UPDATE user_info SET addressCode="{}", latitude="{}", longitude="{}" WHERE openId="{}"'\
            .format(map['id'], map['location']['latitude'], map['location']['longitude'], openid)
        self.inser_update_delete(sql)
        pass

    # 判断用户背景图片颜色深浅
    def judgeimage(self, img):
        img = Image.open(BytesIO(img))
        stat = ImageStat.Stat(img)
        r, g, b = stat.rms
        Y = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        if Y > 0.9:
            return "black"
        else:
            return "white"


if __name__ == '__main__':
    data = {
        'openId': '333',
        'avatarUrl': "https://thirdwx.qlogo.cn/mmopen/vi_32/8O7wCx1X6Whpk5CWDmyUstgJCicHTOn2MfHy6nvAR6FchO0ib9onlQwibKlTMDzB2icDvdI10bqSiaqRibnqMgFBMziaw/132",
        'city': "",
        'country': "",
        'fontcolor': "white",
        'gender': 0,
        'language': "zh_CN",
        'name': "Leisure",
        'nickName': "╰⋛⋋⊱⋋⋌⊰⋌⋚╯",
        'province': "",
        'session_key': '111',
        'state': 0
    }

    time_start = time.time()  # 记录开始时间
    USER().insertOne(data)
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print(time_sum)
