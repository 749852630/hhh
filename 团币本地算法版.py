"""

MK团币本地算法版本
MK偷撸咨询：https://t.me/mktljb
算法没问题参数会的自己改改就能跑明文
CK值只要token便可

"""
import json
import random
import base64
import os
import string
from datetime import datetime
import requests
import time
from functools import partial
from user_agent import generate_user_agent
import concurrent.futures
# 需要 安装pycryptodomex依赖
import re, random, time, base64
from Cryptodome.Util.Padding import unpad
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad


# from flask import Flask, request, jsonify, make_response
# from flask_cors import CORS


# 指纹还原函数
def remove_newlines(text):
    return text.replace('\n', '')


def decrypt_by_public(encrypted_data, key="kwBq8snI"):
    key_bytes = key.encode('utf-8')
    des_key = DES.new(key_bytes, DES.MODE_CBC, key_bytes)
    encrypted_data = remove_newlines(encrypted_data)
    encrypted_bytes = base64.b64decode(encrypted_data)
    decrypted_data = des_key.decrypt(encrypted_bytes)
    decrypted_data = unpad(decrypted_data, DES.block_size)
    decrypted_text = decrypted_data.decode('utf-8')
    return decrypted_text


def replace_between_strings(original_str, start_str, end_str, replacement):
    pattern = re.escape(start_str) + '(.*?)' + re.escape(end_str)
    replaced_str = re.sub(pattern, start_str + replacement + end_str, original_str)
    return replaced_str


def get_between_strings(original_str, start_str, end_str):
    pattern = re.escape(start_str) + '(.*?)' + re.escape(end_str)
    match = re.search(pattern, original_str)
    if match:
        between_str = match.group(1)
        return between_str
    else:
        print("异常 未找到中间值")
        return ""


def getraw(raw, uuid):
    raw = replace_between_strings(raw, '"A28":', ',"A57"', str(int(time.time() * 1000)))
    # 服务器时间
    raw = replace_between_strings(raw, '"A2":', ',"A45"', str(int(time.time() * 1000 + 200)))
    # 电池电量
    raw = replace_between_strings(raw, '"A16":', ',"A21"', str(round(random.uniform(10, 80), 1)))
    # 经纬度
    base_latitude = get_between_strings(raw, '"latitude":', ',"longitude')
    base_longitude = get_between_strings(raw, '"longitude":', '},"A42')
    # uuid
    raw = replace_between_strings(raw, '"A50":"', '","', uuid)
    # 启动时间
    raw = replace_between_strings(raw, '"A40":"', '","', str(int(time.time() * 1000 - 5000)))
    # 生成随机的经度和纬度增量，范围为 -0.005 到 0.005
    latitude_offset = random.uniform(-0.005, 0.005)
    longitude_offset = random.uniform(-0.005, 0.005)
    # 计算新的经纬度坐标
    new_latitude = float(base_latitude) + latitude_offset
    new_longitude = float(base_longitude) + longitude_offset
    raw = replace_between_strings(raw, '"latitude":', ',"longitude', str(round(new_latitude, 7)))
    raw = replace_between_strings(raw, '"longitude":', '},"A42', str(round(new_longitude, 7)))
    # 存储量
    ccl = get_between_strings(raw, '"A46":"', '@')
    random_number = random.randint(int(ccl), int(int(ccl) * 1.01))
    raw = replace_between_strings(raw, '"A46":"', '@', str(random_number))
    return raw


def split_lines(text, line_length):
    return [text[i:i + line_length] for i in range(0, len(text), line_length)]


def add_newlines(text, line_length):
    lines = split_lines(text, line_length)
    return '\n'.join(lines)


def encrypt_by_public(data, key="kwBq8snI"):
    key_bytes = key.encode('utf-8')
    des_key = DES.new(key_bytes, DES.MODE_CBC, key_bytes)
    encrypted_data = des_key.encrypt(pad(data.encode('utf-8'), DES.block_size))
    encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    encrypted_lines = add_newlines(encrypted_base64, 76)
    return encrypted_lines


def sc_uuid():
    current_timestamp = int(time.time()) * 1001
    url = "https://api-unionid.meituan.com/unionid/android/register"

    headers = {
        "Accept-Charset": "UTF-8",
        "uuidRequestId": "2f4570c22850ce5b7217108d23e02f4ab6481abd60198aebb8",
        "uuidSessionId": "3c17844d2677a95e74ad001e31f5d2b8bea5be6ed1567036fd:normal",
        "retrofit_exec_time": f'{current_timestamp}',
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json;charset=UTF-8",
        "Content-Length": "1693",
        "Connection": "Keep-Alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; 10X Build/PQ3A.190801.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 groupTurbo/2.0.202 app/MeituanTurbo",
        "accessToken": "9cG8IvVH696OFxcOycyaKQ",
        "Host": "api-unionid.meituan.com"
    }

    data = {
        "appInfo": {
            "app": "com.meituan.turbo",
            "version": "2.0.202",
            "appName": "meituanturbo",
            "sdkVersion": "1.20.3",
            "userId": "",
            "downloadSource": "turbo_1",
            "privacy": "0"
        },
        "idInfo": {
            "localId": "a5e4744366d9d5345ccd045e801f463257eee25a4a44b41632",
            "uuid": "",
            "requiredId": "4",
            "sessionId": "1c17844d2677a95e74ad001e31f5d2b8bea5be6ed1567036fd:normal",
            "localSessionId": "c458ffb2114d290b87dd98d633c9c97a217c04a11810ccac25"
        },
        "environmentInfo": {
            "platform": "android",
            "osName": "ares-user 9 PQ3A.190801.002 eng.builde.20191015.144423 release-keys",
            "osVersion": "9",
            "clientType": "15",
            "transfer": {
                "uuidTransfer": False,
                "uuidTransferV2": False,
                "uuidTransferV3": False,
                "unionIdTransfer": False,
                "dpidTransfer": False
            },
            "bootIdInfo": {
                "bootId": "V9ACWtFtvh_ArrvyMjycP6DCOXgCTMQyEBvje17AFR8pCyjXkDPdPYypumTKW08K"
            }
        },
        "deviceInfo": {
            "keyDeviceInfo": {},
            "secondaryDeviceInfo": {},
            "brandInfo": {
                "brand": "XIAOMI",
                "deviceModel": "10X"
            }
        },
        "communicationInfo": {},
        "extension": "{\"localUuidInstallNsecTime\":\"\",\"localT\":\"\",\"newInstallNsecTime\":\"\",\"nm\":\"LLKPawO3xWc_MJ3mZeKFbw\",\"nb\":\"z8MKYHeitufcuMGQ8ndddw\",\"pinstalltime\":\"1700756762625\",\"processName\":\"com.meituan.turbo\",\"customAccessNanoTime\":\"1700757728217512437\",\"customCreateNanoTime\":\"1700757728217512437\",\"transferDirInfo\":\"mkdirs\",\"localCustomAccessNanoTime\":\"\",\"localPinstallTime\":\"\",\"localV3T\":\"\",\"localV3CustomNanoTime\":\"\"}",
        "token": "u7Y3d1B_pzvdeUbbjTPTOyJ3Og0c6sLW4_G_V_CT4RpSS7qOJtwmqp_bSddydWZ6WlWYmQ65xqK6Wk_x6t64LqlW_EvCnQ7-89DcRerIrpoummNikImKpAdSLw8Zv4zR37-uzYx-I9DAUDRaAPWlh9T7-bM9N9izVIEJaw544l4",
        "mark": "{\"dpid\":9,\"uuid\":9,\"unionId\":9,\"localId\":129,\"androidId\":13,\"tokeno\":9,\"appid_share\":9,\"appid_local\":135}"
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))

    if r.status_code == 200:
        uuid = r.json()['data']['unionId']
        return uuid
    else:
        return False


class Mttb:
    def __init__(self, zh, ck):
        self.uuid = sc_uuid()
        self.ck = ck
        self.fingerprint="""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\n"""
        self.raw = decrypt_by_public(self.fingerprint, key="kwBq8snI")
        a = encrypt_by_public(getraw(self.raw, self.uuid), key="kwBq8snI")
        b = str(a.encode("utf-8"))
        self.fingerprint = b[2:-1].replace("\\n", "")
        self.fingerprint = self.fingerprint.replace("\n", "")
        # print(self.fingerprint)
        self.lisss = None
        self.lastGmtCreated = None
        self.qdrwids = [10002, 10024, 10041, 10015, 10014]
        self.qdid = None
        self.llid = None
        self.startmsg = ''
        self.endmsg = ''
        self.llids = []
        self.qdactoken = None
        self.num = zh
        self.xtb = None
        self.wcxtb = None
        self.t_h = None
        self.actoken = None
        self.usid = None
        self.name = None
        self.ua = generate_user_agent(os='android')
        self.msg = ""
        self.ids = []
        self.noids = [420, 421, 422, 423, 424, 15169, 15170, 15171, 15172, 15173]
        self.id = None
        self.tid = None
        self.data_list = None

    def login(self):
        try:
            url = "https://open.meituan.com/user/v1/info/auditting?fields=auditAvatarUrl%2CauditUsername"
            h = {
                'Connection': 'keep-alive',
                'Origin': 'https://mtaccount.meituan.com',
                'User-Agent': self.ua,
                'token': self.ck,
                'Referer': 'https://mtaccount.meituan.com/user/',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.9',
                'X-Requested-With': 'com.sankuai.meituan',
            }
            r = requests.get(url, headers=h)
            # print(r.text)
            if 'user' in r.text:
                rj = r.json()
                self.name = rj["user"]["username"]
                # self.name = "plusv"
                self.usid = rj["user"]["id"]

                xx = f'{self.name}   usid:{self.usid}'
                print(xx)
                return True
            else:
                print(r.json())
        except Exception as e:
            print(f'登录异常：{e}')
            exit(0)

    def act(self):
        try:
            url = 'https://game.meituan.com/mgc/gamecenter/front/api/v1/login'
            h = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Length': '307',
                'x-requested-with': 'XMLHttpRequest',
                'User-Agent': self.ua,
                'Content-Type': 'application/json;charset=UTF-8',
                'cookie': f'token={self.ck}'
            }
            sing = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            data = {
                "mtToken": self.ck,
                "deviceUUID": self.uuid,
                "mtUserId": self.usid,
                "idempotentString": sing
            }
            r = requests.post(url, headers=h, json=data)
            if r.json()['data']['loginInfo']['accessToken'] is not None:
                self.actoken = r.json()['data']['loginInfo']['accessToken']
            else:
                print(f'账号{self.num}-{self.name}>>>获取actoken失败：{r.json()}')
        except Exception as e:
            print(f'账号{self.num}-{self.name}>>>获取actoken异常：{e}')
            exit(0)

    def get_ids(self):
        try:
            url = 'https://game.meituan.com/mgc/gamecenter/front/api/v1/mgcUser/task/queryMgcTaskInfo?yodaReady=h5&csecplatform=4&csecversion=2.3.1'
            data = {
                'externalStr': '',
                'riskParams': {
                    "uuid": self.uuid,
                    "platform": 4,
                    "fingerprint": self.fingerprint,
                    "version": "2.0.202",
                    "app": 0,
                    "cityid": "70"
                }
            }
            h = {
                'Accept': 'application/json, text/plain, */*',
                'x-requested-with': 'XMLHttpRequest',
                'User-Agent': self.ua,
                'Content-Type': 'application/json;charset=UTF-8',
                'actoken': self.actoken,
                'mtoken': self.ck,
                'cookie': 'token=' + self.ck
            }
            r = requests.post(url, headers=h, json=data)
            rj = r.json()
            # print(rj)
            if rj['msg'] == 'ok' and r.json()['data']['taskList'] != []:
                self.data_list = r.json()['data']['taskList']
                return True
            else:
                return False
        except Exception as e:
            print(f'账号{self.num}-{self.name}>>>获取任务异常：{e}')
            exit(0)

    def startcxtb(self):
        try_count = 5
        while try_count > 0:
            try:
                url = 'https://game.meituan.com/mgc/gamecenter/skuExchange/resource/counts?sceneId=3&gameId=10102'
                self.t_h = {
                    'User-Agent': self.ua,
                    'actoken': self.actoken,
                    'mtoken': self.ck,
                    'cookie': f'token={self.ck}'
                }
                r = requests.get(url, headers=self.t_h)
                rj = r.json()
                if rj['msg'] == 'ok':
                    data = rj['data']
                    for d in data:
                        self.xtb = d['count']
                        self.startmsg += f'运行前小团币: {int(self.xtb)}({int(self.xtb) / 1000}元)\n'
                    return True
                else:
                    self.startmsg += f'账号{self.num}-{self.name} 查询运行前团币失败：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(3, 8))
                    continue
            except:
                self.startmsg += f'账号{self.num}-{self.name} 查询运行前团币异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def endcxtb(self):
        try_count = 5
        while try_count > 0:
            try:
                url = 'https://game.meituan.com/mgc/gamecenter/skuExchange/resource/counts?sceneId=3&gameId=10102'
                # self.t_h = {
                #     'User-Agent': self.ua,
                #     'actoken': self.actoken,
                #     'mtoken': self.ck,
                #     'cookie': f'token={self.ck}'
                # }
                self.t_h = {
                    'Accept': 'application/json, text/plain, */*',
                    'x-requested-with': 'XMLHttpRequest',
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json;charset=UTF-8',
                    'actoken': self.actoken,
                    'mtoken': self.ck,
                    'cookie': 'token=' + self.ck
                }
                r = requests.get(url, headers=self.t_h)
                rj = r.json()
                if rj['msg'] == 'ok':
                    data = rj['data']
                    for d in data:
                        self.wcxtb = d['count']
                        self.endmsg += f'运行后小团币: {int(self.wcxtb)}({int(self.wcxtb) / 1000}元)\n'
                    return True
                else:
                    self.endmsg += f'账号{self.num}-{self.name} 查询运行后团币失败：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(3, 8))
                    continue
            except:
                self.endmsg += f'账号{self.num}-{self.name} 查询运行后团币异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def b64(self):
        y_bytes = base64.b64encode(self.tid.encode('utf-8'))
        y_bytes = y_bytes.decode('utf-8')
        return y_bytes

    def get_game(self):
        try_count = 5
        while try_count > 0:
            try:
                self.tid = f'mgc-gamecenter{self.id}'
                self.tid = self.b64()
                url = f'https://game.meituan.com/mgc/gamecenter/common/mtUser/mgcUser/task/finishV2?taskId={self.tid}'
                r = requests.get(url, headers=self.t_h)
                if isprint:
                    print(f'领取{self.id} {r.json()}')
                if r.status_code == 200:
                    if r.json()['msg'] == 'ok':
                        time.sleep(random.randint(1, 3))
                        return True
                    elif '完成过' in r.text:
                        time.sleep(random.randint(1, 3))
                        return True
                    else:
                        print(f'账号{self.num}-{self.name} 任务状态: {r.text}')
                        return False
                else:
                    self.endmsg += f'账号{self.num}-{self.name} {self.id}领取任务失败：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(3, 8))
                    continue
            except:
                self.endmsg += f'账号{self.num}-{self.name} {self.id}领取任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def post_id(self):
        try_count = 5
        while try_count > 0:
            try:
                url = 'https://game.meituan.com/mgc/gamecenter/front/api/v1/mgcUser/task/receiveMgcTaskReward?yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig={}'
                data = {
                    "taskId": self.id,
                    "externalStr": "",
                    "riskParams": {
                        "uuid": self.uuid,
                        "platform": 4,
                        "fingerprint": self.fingerprint,
                        "version": "2.0.202",
                        "app": 0,
                        "cityid": "70"
                    }
                }
                r = requests.post(url, headers=self.t_h, json=data)
                if isprint:
                    print(f'完成{self.id} {r.json()}')
                if r.status_code == 200:
                    if r.json()['msg'] == 'ok':
                        time.sleep(random.randint(1, 3))
                        return True
                    elif '异常' in r.text:
                        time.sleep(random.randint(1, 3))
                        return False
                    else:
                        print(f'账号{self.num}-{self.name} {self.id},{r.text}\n')
                        time.sleep(random.randint(1, 3))
                        return False
                else:
                    self.endmsg += f'账号{self.num}-{self.name} {self.id}完成任务异常：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(3, 8))
                    continue
            except:
                self.endmsg += f'账号{self.num}-{self.name} {self.id}完成任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def coin_login(self):
        """获取签到浏览的actoken"""
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Origin': 'https://awp.meituan.com',
                    'Cookie': f'{self.ck}',
                    'Accept': '*/*',
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json',
                    'Host': 'game.meituan.com',
                    'Connection': 'Keep-Alive',
                }
                params = {
                    'mtUserId': self.usid,
                    'mtDeviceId': self.uuid,
                    'mtToken': self.ck,
                    'nonceStr': 'kvb1xnabe4n1cfg1',
                    'gameType': '10273',
                }
                r = requests.get('https://game.meituan.com/coin-marketing/login/loginMgc', headers=headers,
                                 params=params)
                self.qdactoken = r.json().get('accessToken', None)
                if self.qdactoken is not None:
                    return True
                else:
                    print(r.json())
                    return True
            except:
                self.endmsg += f'账号{self.num}-{self.name} 获取异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def qd(self):
        """签到和浏览任务"""
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Host': 'game.meituan.com',
                    'Connection': 'keep-alive',
                    'x-requested-with': 'XMLHttpRequest',
                    'appName': 'meituan',
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Origin': 'https://awp.meituan.com',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                params = {
                    'yodaReady': 'h5',
                    'csecplatform': '4',
                    'csecversion': '2.3.1',
                }

                data = {
                    # "protocolId": 10002,  # 签到
                    # "protocolId": 10024,  # 1 3 5 要等待时间
                    # "protocolId": 10041,  # 下滑浏览
                    # "protocolId": 10008,  # 获取id
                    # "protocolId": 10014,  # 抽奖
                    # "protocolId": 10015,  # 抽奖前运行
                    "protocolId": self.qdid,
                    "data": {},
                    "riskParams": {
                        "uuid": self.uuid,
                        "platform": 4,
                        "fingerprint": self.fingerprint,
                        "version": "2.0.202",
                        "app": 0,
                        "cityid": "70"
                    },
                    "acToken": self.qdactoken,

                }
                if self.qdid == 10024:
                    while True:
                        r = requests.post('https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                                          json=data, params=params)
                        if isprint:
                            print(f'{self.qdid}: {r.json()}')
                        if 'interval' in r.text:
                            xxsj = r.json()['data']['timedReward']['interval']
                            time.sleep(xxsj / 1000)
                            time.sleep(random.randint(1, 3))
                        else:
                            time.sleep(random.randint(1, 3))
                            break
                    return True
                elif self.qdid == 10041:
                    while True:
                        r = requests.post('https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                                          json=data,
                                          params=params)
                        if isprint:
                            print(f'{self.qdid}: {r.json()}')
                        if 'rewardAmount' in r.text:
                            time.sleep(random.randint(1, 3))
                            continue
                        else:
                            time.sleep(random.randint(1, 3))
                            break
                    return True
                else:
                    r = requests.post('https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                                      json=data,
                                      params=params)
                    if isprint:
                        print(f'{self.qdid}: {r.json()}')
                    time.sleep(random.randint(1, 3))
                    return True
            except:
                self.endmsg += f'账号{self.num}-{self.name} {self.qdid}签到任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def get_llids(self):
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Host': 'game.meituan.com',
                    'Connection': 'keep-alive',
                    'x-requested-with': 'XMLHttpRequest',
                    'appName': 'meituan',
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Origin': 'https://awp.meituan.com',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                params = {
                    'yodaReady': 'h5',
                    'csecplatform': '4',
                    'csecversion': '2.3.1',
                }

                data = {
                    # "protocolId": 10002,  # 签到
                    # "protocolId": 10024,  # 1 3 5 要等待时间
                    # "protocolId": 10041,  # 下滑浏览
                    # "protocolId": 10008,  # 获取id
                    # "protocolId": 10014,  # 抽奖
                    # "protocolId": 10015,  # 抽奖前运行
                    "protocolId": 10008,
                    "data": {},
                    "riskParams": {
                        "uuid": self.uuid,
                        "platform": 4,
                        "fingerprint": self.fingerprint,
                        "version": "2.0.202",
                        "app": 0,
                        "cityid": "70"
                    },
                    "acToken": self.qdactoken,

                }

                r = requests.post('https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                                  json=data,
                                  params=params)
                time.sleep(random.randint(1, 3))
                self.lisss = r.json()['data']['taskInfoList']
                return True
            except:
                self.endmsg += f'账号{self.num}-{self.name} {self.qdid}签到任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def get_ll(self):
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Host': 'game.meituan.com',
                    'Connection': 'keep-alive',
                    'x-requested-with': 'XMLHttpRequest',
                    'appName': 'meituan',
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Origin': 'https://awp.meituan.com',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                params = {
                    'yodaReady': 'h5',
                    'csecplatform': '4',
                    'csecversion': '2.3.1',
                }

                get_data = {
                    "protocolId": 10010,  # 先运行获取任务
                    "data": {
                        "externalStr": {"cityId": "351"},
                        "taskId": self.llid,  # 任务id
                        "taskEntranceType": "normal"
                    },
                    "riskParams": {
                        "uuid": self.uuid,
                        "platform": 4,
                        "fingerprint": self.fingerprint,
                        "version": "2.0.202",
                        "app": 0,
                        "cityid": "70"
                    },
                    "acToken": self.qdactoken,
                    "mtToken": self.ck
                }
                r = requests.post(
                    'https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                    json=get_data,
                    params=params
                )
                if isprint:
                    print(f'{self.llid} 领取任务 {r.json()}')
                if r.json()['data'] is None:
                    time.sleep(random.randint(1, 3))
                    return False
                else:
                    time.sleep(random.randint(1, 3))
                    return True
            except:
                self.endmsg += f'账号{self.num}-{self.name} {self.llid}获取浏览任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def post_ll(self):
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Host': 'game.meituan.com',
                    'Connection': 'keep-alive',
                    'x-requested-with': 'XMLHttpRequest',
                    'appName': 'meituan',
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Origin': 'https://awp.meituan.com',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                params = {
                    'yodaReady': 'h5',
                    'csecplatform': '4',
                    'csecversion': '2.3.1',
                }

                post_data = {
                    "protocolId": 10009,  # 再运行完成任务
                    "data": {
                        "externalStr": {"cityId": "351"},
                        "taskId": self.llid,  # 任务id
                        "taskEntranceType": "normal"
                    },
                    "riskParams": {
                        "uuid": self.uuid,
                        "platform": 4,
                        "fingerprint": self.fingerprint,
                        "version": "2.0.202",
                        "app": 0,
                        "cityid": "70"
                    },
                    "acToken": self.qdactoken,
                    "mtToken": self.ck
                }

                r = requests.post(
                    'https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                    json=post_data,
                    params=params
                )
                if isprint:
                    print(f'{self.llid} 完成任务 {r.json()}\n')
                if r.json()['data'] is None:
                    time.sleep(random.randint(1, 3))
                    return False
                else:
                    time.sleep(random.randint(1, 3))
                    return True
            except:
                self.endmsg += f'账号{self.num}-{self.name} {self.llid}完成浏览任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def tj_bchd(self):
        try_count = 5
        while try_count > 0:
            try:
                bchd = int(self.wcxtb) - int(self.xtb)
                url = "https://game.meituan.com/mgc/gamecenter/skuExchange/resources/change/logs?changeType=1&limit=50&sceneId=2&gameId=10139&mtToken=&acToken=&shark=1&yodaReady=h5&csecplatform=4&csecversion=2.3.1"
                headers = {
                    "Host": "game.meituan.com",
                    "Connection": "keep-alive",
                    "x-requested-with": "XMLHttpRequest",
                    "actoken": self.qdactoken,
                    "mtoken": self.ck,
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13; V2055A Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.74 Mobile Safari/537.36 TitansX/11.38.10 KNB/1.2.0 android/13 mt/com.meituan.turbo/2.0.202 App/10120/2.0.202 MeituanTurbo/2.0.202",
                    "Content-Type": "application/json",
                    "Accept": "*/*",
                    "Origin": "https://awp.meituan.com",
                    "Sec-Fetch-Site": "same-site",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://awp.meituan.com/",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"

                }
                r = requests.get(url, headers=headers)
                if 'ok' in r.text:
                    datalist = r.json()['data']
                    coins = 0
                    for data in datalist:
                        coin = data['changeCount']
                        gmtCreated = data['gmtCreated']
                        if gmtCreated >= f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00":
                            coins += coin
                        else:
                            break
                    self.lastGmtCreated = datalist[-1]['gmtCreated']
                    while True:
                        if self.lastGmtCreated >= f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00":
                            url1 = f"https://game.meituan.com/mgc/gamecenter/skuExchange/resources/change/logs?changeType=1&limit=50&sceneId=2&lastGmtCreated={self.lastGmtCreated}&gameId=10139&mtToken=&acToken=&shark=1&yodaReady=h5&csecplatform=4&csecversion=2.3.1"
                            r = requests.get(url1, headers=headers)
                            if 'ok' in r.text:
                                datalist = r.json()['data']
                                for data in datalist:
                                    coin = data['changeCount']
                                    gmtCreated = data['gmtCreated']
                                    if gmtCreated >= f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00":
                                        coins += coin
                                    else:
                                        break
                                self.lastGmtCreated = datalist[-1]['gmtCreated']
                                if self.lastGmtCreated >= f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00":
                                    time.sleep(random.randint(1, 3))
                                    continue
                                else:
                                    self.endmsg += f'本次获得小团币: {bchd}\n今日团币: {coins}'
                                    return True
                            else:
                                self.endmsg += f'账号{self.num}-{self.name} 获取今日团币异常：还有{try_count - 1}次重试机会\n'
                                try_count -= 1
                                time.sleep(random.randint(2, 5))
                                continue
                        else:
                            self.endmsg += f'本次获得小团币: {bchd}\n今日团币: {coins}'
                            return True
                    break
                else:
                    self.endmsg += f'账号{self.num}-{self.name} 获取今日团币异常：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(2, 5))
                    continue
            except:
                self.endmsg += f'账号{self.num}-{self.name} 获取今日团币异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(2, 5))
                continue

    def get_new_gameid(self):
        if self.get_ids():
            self.ids = []
            zt_3 = []
            for i in self.data_list:
                if i['status'] == 2 and i['id'] not in self.noids:
                    self.ids.append(i['id'])
                if i['status'] == 3 and i['id'] not in self.noids:
                    self.ids.append(i['id'])
                    zt_3.append(i['id'])
                else:
                    pass
            if isprint:
                print(f'获取到{len(self.ids)}个任务！\n{self.ids}')
            if self.ids != [] and len(zt_3) < 10:
                return True
            elif not self.ids:
                return True
            else:
                return False
        else:
            return False

    def run_game(self):
        for i in self.data_list:
            self.id = i['id']
            zt = i['status']
            if self.id in self.noids:
                pass
            else:
                if zt == 2:
                    if isprint:
                        print(f'id: {self.id} 状态: {zt}')
                    if self.get_game():
                        self.post_id()
                        if isprint:
                            print()
                        continue
                elif zt == 3:
                    if isprint:
                        print(f'id: {self.id} 状态: {zt}')
                    self.post_id()
                    if isprint:
                        print()
                    continue
                else:
                    continue

    def get_new_llids(self):
        if self.get_llids():
            self.llids = []
            for i in self.lisss:
                zt = i['status']
                if zt == 2 and i['id']:
                    self.llids.append(i['id'])
                elif zt == 3 and i['id']:
                    self.llids.append(i['id'])
                else:
                    pass
            if isprint:
                print(f'获取到{len(self.llids)}个任务！\n{self.llids}')
            if self.llids:
                return True
            else:
                return False
        else:
            return False

    def run_tbzx(self):
        for i in self.lisss:
            zt = i['status']
            self.llid = i['id']
            taskTitles = json.loads(i['mgcTaskBaseInfo']['viewExtraJson'])
            taskTitle = taskTitles['common']['taskTitle']
            taskDesc = taskTitles['common']['taskDesc']
            if zt in [2, 3] and self.llid == 15181:
                if isprint:
                    print(f'{self.llid}: 状态：{zt} {taskTitle}({taskDesc})')
                while True:
                    if self.get_ll():
                        if self.post_ll():
                            continue
                        else:
                            break
                    else:
                        break
            elif zt == 2:
                if isprint:
                    print(f'{self.llid}: 状态：{zt} {taskTitle}({taskDesc})')
                if self.get_ll():
                    self.post_ll()
            elif zt == 3:
                if isprint:
                    print(f'{self.llid}: 状态：{zt} {taskTitle}({taskDesc})')
                self.post_ll()
            else:
                pass

    def main(self):
        if self.login():
            self.act()
            if self.startcxtb():
                isgame = self.get_new_gameid()
                if isgame and self.ids != []:
                    self.startmsg += f'🔔游戏中心获取任务成功！🚀即将运行游戏中心任务和团币中心任务\n'
                    print(self.startmsg)
                    while True:
                        self.run_game()
                        if self.get_new_gameid() and len(self.ids) != 0:
                            continue
                        else:
                            break
                    if self.coin_login():
                        for i in self.qdrwids:
                            self.qdid = i
                            self.qd()
                        if self.get_new_llids():
                            self.run_tbzx()
                        self.endmsg += f'账号{self.num}-{self.name}({self.usid}) 🎉运行完成\n'
                        if self.endcxtb():
                            if self.tj_bchd():
                                print(self.endmsg)
                elif isgame and self.ids == []:
                    self.startmsg += f'✅游戏中心已经全部完成！🚀即将运行团币中心任务\n'
                    print(self.startmsg)
                    if self.coin_login():
                        for i in self.qdrwids:
                            self.qdid = i
                            self.qd()
                        if self.get_new_llids():
                            self.run_tbzx()
                        self.endmsg += f'账号{self.num}-{self.name}({self.usid}) 🎉运行完成\n'
                        if self.endcxtb():
                            if self.tj_bchd():
                                print(self.endmsg)
                else:
                    self.startmsg += f'💔游戏中心获取任务失败！🚀即将运行团币中心任务\n'
                    print(self.startmsg)
                    if self.coin_login():
                        for i in self.qdrwids:
                            self.qdid = i
                            self.qd()
                        if self.get_new_llids():
                            self.run_tbzx()
                        self.endmsg += f'账号{self.num}-{self.name}({self.usid}) 🎉运行完成\n'
                        if self.endcxtb():
                            if self.tj_bchd():
                                print(self.endmsg)


if __name__ == '__main__':
    print = partial(print, flush=True)
    print('🔔MK自用算法版本1.1')
    # 是否打印详细日志
    isprint = False

    token = os.environ.get("mtxtbck")


    if token is None:
        print(f'⛔️未获取到ck变量：请检查变量是否填写')
        exit(0)
    if '&' in token:
        tokens = token.split('&')
    else:
        tokens = [token]

    bf = os.environ.get("xtbbf")
    bf = 8
    if bf is None:
        print(f'⛔️为设置并发变量，默认1')
        bf = 1

    print(f'✅获取到{len(tokens)}个账号')
    print(f'🔔设置最大并发数: {bf}\n')

    with concurrent.futures.ThreadPoolExecutor(max_workers=int(bf)) as executor:
        print(f'======================================')
        for num in range(len(tokens)):
            runzh = num + 1
            run = Mttb(runzh, tokens[num])
            executor.submit(run.main)
            time.sleep(random.randint(2, 5))
