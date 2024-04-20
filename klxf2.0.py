#变量KL_COOKIES：小程序抓authorization的值，多ck换行
#变量KL_CODES：买的可乐码，多码换行

import requests
import os
import json
import random
import time
def get_weather():
    # 假设有一个包含所有中国城市名称的列表
    china_cities = [
        "北京市", "上海市", "广州市", "深圳市", "杭州市", "南京市", "重庆市", "成都市", "天津市", "西安市", "苏州市", "武汉市", "长沙市", "青岛市", "郑州市", "沈阳市", "大连市", "厦门市", "合肥市", "昆明市", "济南市", "宁波市", "福州市", "哈尔滨市", "长春市", "石家庄市", "贵阳市", "南宁市", "太原市", "乌鲁木齐市", "兰州市", "海口市", "西宁市", "银川市", "呼和浩特市", "拉萨市", "唐山市", "无锡市", "佛山市", "南通市", "东莞市", "温州市", "徐州市", "嘉兴市", "烟台市", "惠州市", "绍兴市", "常州市", "珠海市", "中山市", "金华市", "廊坊市", "保定市", "台州市", "沧州市", "济宁市", "洛阳市", "盐城市", "扬州市", "泰州市", "临沂市", "潍坊市", "邯郸市", "江门市", "汕头市", "芜湖市", "济宁市", "淄博市", "咸阳市", "阜阳市", "宜昌市", "包头市", "许昌市", "荆州市", "襄阳市", "鄂尔多斯市", "常德市", "孝感市", "张家口市", "六安市", "齐齐哈尔市", "乐山市", "临汾市", "南充市", "榆林市", "丹东市", "延边朝鲜族自治州", "阳泉市", "赤峰市", "黄石市", "德州市", "眉山市", "盘锦市", "曲靖市", "丽水市", "抚顺市", "萍乡市", "营口市", "三明市", "上饶市", "景德镇市", "怀化市", "商丘市", "揭阳市", "肇庆市", "长治市", "焦作市", "朝阳市", "新乡市", "通辽市", "佳木斯市", "平顶山市", "忻州市", "永州市", "毕节市", "潮州市", "白山市", "伊犁哈萨克自治州", "黔东南苗族侗族自治州", "吉安市", "鹤壁市", "达州市", "百色市", "铜仁市", "本溪市", "铁岭市", "吕梁市", "石嘴山市", "辽阳市", "随州市", "鸡西市", "巴彦淖尔市", "防城港市", "黔南布依族苗族自治州", "临夏回族自治州", "黑河市", "双鸭山市", "楚雄彝族自治州", "昭通市", "铜陵市", "阿拉善盟", "乌兰察布市", "贵港市", "普洱市", "庆阳市", "酒泉市", "海西蒙古族藏族自治州", "锡林郭勒盟", "定西市", "阿坝藏族羌族自治州", "昌吉回族自治州", "白城市", "保山市", "塔城地区", "呼伦贝尔市", "固原市", "甘孜藏族自治州", "怒江傈僳族自治州", "伊犁哈萨克自治州", "大兴安岭地区", "迪庆藏族自治州", "果洛藏族自治州", "玉树藏族自治州", "海南藏族自治州", "海北藏族自治州", "黄南藏族自治州", "阿里地区", "那曲地区", "山南市", "克孜勒苏柯尔克孜自治州", "和田地区", "喀什地区", "塔城地区", "博尔塔拉蒙古自治州", "昌吉回族自治州", "巴音郭楞蒙古自治州", "阿勒泰地区", "哈密市", "吐鲁番市", "克拉玛依市"
    ]

    # 生成一个随机市名
    random_city = random.choice(china_cities)
    cookies = {
        'search_gray': '0',
        'home_gray': '1',
        'tfstk': 'ffd-af06Kmmkxh9HnUMDLaC1XZggwBLzD38_tMjudnKvbheHEHfkRWLdm4WoU6vAvntAVWflZ2ICceTkZ30PdzRvXWVo4Y8Q91fIjccisU8lT6iiBSQksu7NRkGhFaGfKpHn2ccisUTPT6iij2zRdVIhR6a5V6gAGabhOJ_WAi6f5Nq5O6tBlqQdyawQO8sjGNQiOQeRYJSQ9IocoZMTF4VUTIQfYa8xDS7BLaERAEsAuZRYbTI6PiFnfpOySMI21mDvu3vWqZ-K6mCe0ptCJnZjxT8BHnQJqcEFxQ8k9Z8-FDLOwKdAZQiUQEYAVOCDnxolK_KJQGWS3m-1BFvGaCiY1MpW4HWwtcPPVeTw_dfti816kpt9pgWXsCUgRljO-83vOJyFFZxIQfDV8RaNmZIioE2ULtD_t8dnzJwQb5bAjqjLLJWms',
        'cna': 'cmCkHvwAZlUCAXrOvi3bfpve',
        'isg': 'BAIC7wy_0MCa68wcDuQUs_LOUAhk0wbt5WbBCEwcrnUgn7wZK2LO_ReZTxvj1H6F',
        'Hm_lvt_c8ac07c199b1c09a848aaab761f9f909': '1713205872',
        'Hm_lpvt_c8ac07c199b1c09a848aaab761f9f909': '1713205880',
        'xlly_s': '1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://developer.amap.com/tools/picker',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'search_gray=0; home_gray=1; tfstk=ffd-af06Kmmkxh9HnUMDLaC1XZggwBLzD38_tMjudnKvbheHEHfkRWLdm4WoU6vAvntAVWflZ2ICceTkZ30PdzRvXWVo4Y8Q91fIjccisU8lT6iiBSQksu7NRkGhFaGfKpHn2ccisUTPT6iij2zRdVIhR6a5V6gAGabhOJ_WAi6f5Nq5O6tBlqQdyawQO8sjGNQiOQeRYJSQ9IocoZMTF4VUTIQfYa8xDS7BLaERAEsAuZRYbTI6PiFnfpOySMI21mDvu3vWqZ-K6mCe0ptCJnZjxT8BHnQJqcEFxQ8k9Z8-FDLOwKdAZQiUQEYAVOCDnxolK_KJQGWS3m-1BFvGaCiY1MpW4HWwtcPPVeTw_dfti816kpt9pgWXsCUgRljO-83vOJyFFZxIQfDV8RaNmZIioE2ULtD_t8dnzJwQb5bAjqjLLJWms; cna=cmCkHvwAZlUCAXrOvi3bfpve; isg=BAIC7wy_0MCa68wcDuQUs_LOUAhk0wbt5WbBCEwcrnUgn7wZK2LO_ReZTxvj1H6F; Hm_lvt_c8ac07c199b1c09a848aaab761f9f909=1713205872; Hm_lpvt_c8ac07c199b1c09a848aaab761f9f909=1713205880; xlly_s=1',
    }

    params = [
        ('platform', 'JS'),
        ('s', 'rsv3'),
        ('logversion', '2.0'),
        ('key', 'f7d40927ba4d64fb91ebe2bb9cda0995'),
        ('sdkversion', '2.0.5.25'),
        ('appname', 'https%3A%2F%2Fdeveloper.amap.com%2Ftools%2Fpicker'),
        ('csid', 'C0893945-00CC-439B-B154-95C0822C1721'),
        ('city', '110000'),
        ('page', '1'),
        ('offset', '1'),
        ('extensions', 'all'),
        ('language', 'zh_cn'),
        ('s', 'rsv3'),
        ('children', ''),
        ('type_', 'KEYWORD'),
        ('antiCrab', 'true'),
        ('keywords', random_city),
        ('callback', 'jsonp_199201_1713205932365_'),
    ]

    response = requests.get('https://developer.amap.com/AMapService/v3/place/text', params=params, cookies=cookies, headers=headers)
    # 去掉前缀 "jsonp_199201_1713205932365_(" 和末尾 ")"\
    a=response.text
    json_data = a[28:-1]
    # 解析JSON字符串为Python字典
    data_dict = json.loads(json_data)

    # 提取“pois”列表中的第一个元素（即“郑州东站”的信息）
    zdz_info = data_dict["pois"][0]
    return [float(zdz_info["location"].split(",")[0]+'999104817708'),float(zdz_info["location"].split(",")[1]+'213677300347'),random_city]

def send_scan_draw_request(authorization, pincode,num,i):
    url = "https://koplus.icoke.cn/cre-bff/wechat/user/lotteries/G/scan-draw"
    a=get_weather()
    # Remaining headers and payload fields
    headers = {
        "Connection": "keep-alive",
        "charset": "utf-8",
        "x-sg-signature": "1ad29c1311d4ee0807636c6a76cbea36354e8577c041209793b5462381081e8d",
        "sv": "2",
        "x-sg-timestamp": str(int(time.time() * 1000)),
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Zoom Edition Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160117 MMWEBSDK/20231202 MMWEBID/7075 MicroMessenger/8.0.47.2560(0x28002F30) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "content-type": "application/json",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Referer": "https://servicewechat.com/wxa5811e0426a94686/381/page-frame.html",
    }

    # Update the authorization header with the passed argument
    headers["authorization"] = authorization

    # Define the payload with the passed pincode
    payload = {
        "pincode": pincode,
        "isAuthLbs": True,
        "latitude": a[1],
        "longitude": a[0],
        "accuracy": 30,
        "altitude": 0,
        "speed": 0,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        
        print(f"🥤定位：{a[2]} 第{response.json()['data']['dailyDrawnCount']}次扫码成功,结果：{response.json()['data']['brand']}")
        return True
    elif response.status_code == 400:
        print(f'🥤定位：{a[2]} 第{i+1}次扫码失败，原因：码子被操了，下一个')
        
        i=-1
        return True
    elif response.status_code == 406:
        print(f'🥤定位：{a[2]} 第{i+1}次扫码失败，原因：抽奖次数用完。')
        return False
    elif response.status_code == 401:
        print(f'🥤定位：{a[2]} 第{i+1}次扫码失败，原因：错误的CK。')
        return False
    else:
        print(f"未知错误：{response.status_code}：{response.text},发给作者")
        return False

klcks = os.getenv("KL_COOKIES").split("\n")

codes = os.getenv("KL_CODES").split("\n")

global num
num=0
global i
print("=====可乐瓶盖  By:Write or ... =====")
try:
    for y in range(len(klcks)):
        ck = klcks[y]
        print(f'🥤第{y+1}个账号开始')
        if num<=len(codes):
            for i in range(3):
                    if send_scan_draw_request(ck, codes[num],num,i):
                        pass
                    else:
                        break
                    num=num+1
        else:
            print("🥤码子不够用了，去买码子吧")
            break
except:
    print("🥤码子不够用了，去买码子吧")