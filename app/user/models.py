from tools.db import DB
from PIL import Image, ImageStat
from io import BytesIO
import time


class USER(DB):
    def __init__(self):
        DB.__init__(self)
        self.table_name = 'user_info'

    def find_by_userid(self, userid):
        sql = 'SELECT * FROM user_info WHERE userId = "{}"'.format(userid)
        return self.select_one(sql)

    def finduserbyopenid(self, openid):
        sql = 'SELECT * FROM user_info WHERE openId = "{}"'.format(openid)
        return self.select_one(sql)

    def insertOne(self, data):
        sql = 'INSERT INTO user_info(openId, sessionKey, nickName, avatarUrl, city, gender, province, ' \
              'district, language) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.\
            format(data['openId'], data['sessionKey'], data['nickName'], data['avatarUrl'], data['city'],
                   data['gender'], data['province'], data['district'], data['language'])
        self.insert_update_delete(sql)

    def updatebyuserid(self, map, openid):
        sql = 'UPDATE user_info SET addressCode="{}", latitude="{}", longitude="{}", province="{}",' \
              'city="{}", district="{}" WHERE openId="{}"'\
            .format(map['id'], map['latitude'], map['longitude'], map['province'], map['city'], map['district'], openid)
        self.insert_update_delete(sql)
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
    user = USER()
    data = {
        'openId': '',
        'avatarUrl': "",
        'city': "",
        'district': "",
        'fontcolor': "",
        'gender': 0,
        'language': "",
        'name': "",
        'nickName': 'tttt',
        'province': "",
        'sessionKey': '',
        'state': 0
    }

    time_start = time.time()  # 记录开始时间
    # for i in range(0, 10):
    #     data['nickName'] = 'test'+str(i)
    user.insertOne(data)
    print(user.select_latest_after_insert('user_info', 'userId'))
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print(time_sum)
