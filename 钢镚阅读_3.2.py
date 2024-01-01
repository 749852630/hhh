"""
💰 钢镚阅读_V3.2    ♻20231128

🔔 阅读赚金币，金币可提现，每天最低1—2元，邀请好友还可以赚更多，本脚本自动推送检测文章到微信，需要用户手动阅读过检测，过检测后脚本自动完成剩余任务，每天180篇，每篇100金币，3000金币可提现，提现秒到账，10000金币=1元。不需要下载app，在微信打开下方链接即可进入到活动页。

🔔 为了您能持久获得收益，请仔细阅读以下说明

👉 活动入口 微信打开： http://w.6mcyrj8t2qnq.cloud/?p=2570519    备用链接：https://tinyurl.com/3rcek97w   建议将链接添加至微信收藏，或添加到悬浮窗，方便进入查看和阅读检测文章

@进入后点击永久入口，保存二维码，当链接失效时扫码获取最新链接！

@建议一个微信号只运行一个阅读任务，否则会被列入风险用户，导致阅读无效，得不偿失！

@运行脚本前建议手动阅读5篇左右再使用脚本，不然100%黑！！！

@本脚本仅供学习交流，请在下载后的24小时内完全删除 请勿用于商业用途或非法目的，否则后果自负。

提示：
建议使用“pushplus推送加”接收检测文章，微信公众号关注“pushplus推送加”，点击pushplus进入到官网首页注册并激活消息，注册后获取您token口令填写到下方(key=" ")。当然您也可以使用企业微信接收消息。
每天前两篇检测文章不过，有黑号的风险，导致阅读无效，如不能及时接收检测文章，或不能及时阅读检测文章，建议手动运行脚本，运行前去微信手动阅读三篇文章，每篇阅读6秒以上。
每天180个任务不建议跑满，细水长流，如出现阅读更新中，你的账号可能风险，建议24小时后再操作，平时在订阅号多读文章，多点赞评论，可以减小黑号的几率。
为了阅读账号安全，调试过程严谨反复运行脚本，可间隔2小时进行第二次调试，调试运行前应检查好各参数配置。

推送：(三选一)
检测文章推送参数支持（环境变量），也可填到下方 "" 中。
1. 企业微信推送 
wechatBussinessKey 企业微信webhook机器人后面的 key
2. wxpusher推送
wxpusherAppToken 填wxpusher的appToken
wxpusherTopicId  # 这个是wxpusher的topicId改成你自己的
具体使用方法请看文档地址：https://wxpusher.zjiecode.com/docs/#/
3. pushplus推送加
pushpluskey  填写pushplus推送加的Token口令，请微信登录官方网站注册获取

参数：
阅读文章时用抓包工具抓出cookie（搜索gfsessionid关键词），获取参数cookie，同时获取 User-Agent 填到下方 UA = ""
变量名称：ydtoken     变量值：gfsessionid=o-0fIv9cGv3xxxxxxx; zzbb_info=%7B%22xxxxxxx
多账号用'&'隔开  例:账号1&账号2
      
定时:
自动定时规则cron： 0 7-23/3 * * *   (每天7-23点每3小时一次)，期间注意接收微信通知，阅读检测文章，(key参数必填)
手动定时规则cron： 0                (不自动运行)，每次手动运行脚本时务必注意阅读检测文章，每篇阅读6秒以上。

👉必填的参数 (ydtoken，填到环境变量；UA，环境变量或下方""内；推送三选一的token或key，环境变量或下方 "" 内)

"""

import random
import hashlib
import json
import os
import time
import requests
import threading
from multiprocessing import Pool, freeze_support
from multiprocessing.pool import ThreadPool
lock = threading.Lock()

#以下参数填写到环境变量时()内为变量名称，变量值为抓包或各推送平台获取。也可直接填到 "" 内。
#如：变量名：UA   变量值：Mozilla/5.0 (Linux; Android 9; V1923A xxxxxx
#    或直接填到 "" 内，例：UA = os.getenv("UA") or "Mozilla/5.0 (Linux; Android 9; V1923A xxxxxx"

#抓包获取User-Agent(🔔必填)，(支持环境变量)(必须为微信的User-Agent)
UA = os.getenv("UA") or "" 
# wxpusher推送，填wxpusher的appToken
wxpusherAppToken = os.getenv("wxpusherAppToken") or ""
wxpusherTopicId = os.getenv("wxpusherTopicId") or ""
# 企业微信推送，填企业微信机器人webhook的key
wechatBussinessKey = os.getenv("wechatBussinessKey") or ""
# pushplus加推送，填写pushpluskey+的Token口令
pushpluskey = os.getenv("pushpluskey") or ""
# 并发线程数(建议3线程)
theadNumber = 3 
# 等待检测文章的延时区间，默认等待 15 - 20s 的随机时间，请在该时间内完成检测文章阅读
delayMiniTime = 30
delayMaxTime = 60
# 限制只有自己的下级方可自动阅读过检测，(False  or  True)
onlyChildrenAutoRead = True
# 限制自动检测的账号起始坐标（在这个之前的账号不检测是否为下级），注意：在 conc 和 desi 的情况下会异常，请改为 0
disabledCheckAccountIndex = 100
# 我的邀请id，根据这个检查是否是自己的下级
myInviteId = "2585865"
# 微信自动提现开关 1开启 0关闭
money_Withdrawal = 0


def getParentId(cookie, accountIndex):
    print(f"\n=======💚开始查询 账号【{accountIndex}】上级信息💚=======")
    current_time = str(int(time.time()))
    # 计算 sign
    sign_str = f"key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={current_time}"
    sha256_hash = hashlib.sha256(sign_str.encode())
    sign = sha256_hash.hexdigest()
    url = "http://2585865.neavbkz.jweiyshi.r0ffky3twj.cloud/person/info"
    headers = {
        "User-Agent": UA,
        "Cookie": cookie,
    }

    data = {"time": current_time, "sign": sign}
    response = {}
    try:
        result = requests.get(url, headers=headers, json=data)
        if result:
            response = result.json()
            if response["code"] == 0:
                parentId = response["data"]["pid"]
                return parentId
    except Exception as e:
        # 处理异常
        print(f"提示：", " 账号【{i}】获取上级信息失败", e)
        return


def main_task(accountData, accountIndex):
    global wechatBussinessKey, wxpusherAppToken, wxpusherTopicId
    # 按@符号分割当前账号的不同参数
    values = accountData.split("@")
    if len(values) == 2:
        cookie, wechatBussinessKey = values[0], values[1]
    else:
        cookie = values[0]
    findParentId = 0
    autoSkipRead = True
    # 如果当前坐标大于等于检测的坐标，说明需要检测
    if disabledCheckAccountIndex <= accountIndex:
        findParentId = getParentId(cookie, accountIndex)
        print(
            f"\n账号【{accountIndex}】找到的上级ID：{findParentId} 与 我的邀请ID：{myInviteId} 不符，将禁止推送到自动阅读！"
        )
        if findParentId:
            if findParentId == myInviteId:
                autoSkipRead = True
            else:
                autoSkipRead = False
        else:
            autoSkipRead = False
    else:
        print(f"\n账号【{accountIndex}】不在检测范围内，不检测上下级关系")
    # 输出当前正在执行的账号
    print(f"\n=======💚开始执行 账号【{accountIndex}】阅读任务💚=======")
    current_time = str(int(time.time()))

    # 计算 sign
    sign_str = f"key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={current_time}"
    sha256_hash = hashlib.sha256(sign_str.encode())
    sign = sha256_hash.hexdigest()
    url = "http://2585865.neavbkz.jweiyshi.r0ffky3twj.cloud/share"
    headers = {
        "User-Agent": UA,
        "Cookie": cookie,
    }

    data = {"time": current_time, "sign": sign}
    response = {}
    try:
        result = requests.get(url, headers=headers, json=data)
        if result:
            print()
        else:
            result = requests.get(url, headers=headers, json=data)
        if result:
            response = result.json()
            share_link = response["data"]["share_link"][0]
            myUserId = share_link.split("=")[1].split("&")[0]
            # 如果当前用户是自己，肯定跳过啦
            if myUserId == findParentId:
                autoSkipRead = True
            url = "http://2585865.neavbkz.jweiyshi.r0ffky3twj.cloud/read/info"
            result = requests.get(url, headers=headers, json=data)
            if result:
                response = result.json()
            else:
                result = requests.get(url, headers=headers, json=data)
                response = result.json()
            if result.json()["code"] == 0:
                print(
                    f" 账号【{accountIndex}】获取任务成功，今日已赚：",
                    result.json()["data"]["gold"],
                )
            else:
                print(
                    f" 账号【{accountIndex}】获取任务信息出错：",
                    result.json()["message"],
                )
        else:
            print(f" 账号【{accountIndex}】未获取到share信息：", result.text)
            return
        if response["code"] == 0:
            remain = response["data"]["remain"]
            read = response["data"]["read"]
            print(
                f" 账号【{accountIndex}】ID:{myUserId}----💰钢镚余额：{remain}    今日阅读：{read}"
            )
        else:
            print(f" 账号【{accountIndex}】获取用户信息失败：", response["message"])
    except Exception as e:
        # 处理异常
        print(f"提示：", " 账号【{i}】失败，请检查你的Cookies", e)
        return
    # 如果关闭了限制检查，则前面的判断无效，全部推翻
    if onlyChildrenAutoRead == False:
        autoSkipRead = True
    print(f"============📖开始阅读 账号【{accountIndex}】📖============")
    for readIndex in range(30):
        biz_list = [
            "MzkyMzI5NjgxMA==",
            "MzkzMzI5NjQ3MA==",
            "Mzg5NTU4MzEyNQ==",
            "Mzg3NzY5Nzg0NQ==",
            "MzU5OTgxNjg1Mg==",
            "Mzg4OTY5Njg4Mw==",
            "MzI1ODcwNTgzNA==",
            "Mzg2NDY5NzU0Mw==",
            "MzA4OTI3ODY4Mg=",
            "MzAwNTIzNjYzNA==",
            "Mzg4NjY5NzE4NQ==",
            "MzkwODI5NzQ4MQ==",
            "MzkzMzI5Njc0Nw==",
            "Mzg5NDg5MDY3Ng==",
            "MzA3MjMwMTYwOA==",
            "MzkyNTM5OTc3OQ==",
            "MjM5OTQ0NzI3Ng==",
            "MzkwOTU3MDI1OA==",
            "MzAwOTc2NDExMA==",
            "MzA3OTI4MDMxMA==",
            "MzkxNzI2ODcwMQ==",
            "MzA3MDMxNzMzOA==",
            "Mzg3NjAwODMwMg==",
            "MzI3NDE2ODk1Nw==",
            "MzIyMDMyNTMwMw==",
            "MzIzMjY2NTMwNQ==",
            "MzkxNzMwMjY5Mg==",
            "MzA5Njg3MDk2Ng==",
            "MzA5MzM1OTY2OQ==",
            "MzA4NTQwNjc3OQ==",
            "MjM5NTY5OTU0MQ==",
            "MzU1NTc4OTg2Mw==",
            "MzkwMzI0NjQ4Mw==",
            "MzI3OTA2NDk0Nw==",
            "MjM5MDU4ODgwMw==",
            "Mzg4NzUyMjQxMw==",
        ]
        # 计算 sign
        sign_str = (
            f"key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={current_time}"
        )
        sha256_hash = hashlib.sha256(sign_str.encode())
        sign = sha256_hash.hexdigest()
        url = "http://2585865.9o.10r8cvn6b1.cloud/read/task"

        try:
            response = requests.get(url, headers=headers, json=data, timeout=7).json()
        except requests.Timeout:
            print(f" 账号【{accountIndex}】❗第{readIndex+1}次阅读请求超时，尝试重新发送请求...")
            response = requests.get(url, headers=headers, json=data, timeout=7).json()
        if response["code"] == 1:
            print(f" 账号【{accountIndex}】第{readIndex+1}次阅读结果：", response["message"])
            break
        else:
            try:
                # print("返回：", response["data"])
                postUrl = response["data"]["link"]
                if postUrl:
                    try:
                        mid = postUrl.split("&mid=")[1].split("&")[0]
                        biz = postUrl.split("__biz=")[1].split("&")[0]
                    except Exception as e:
                        url = response["data"]["link"]

                        try:
                            result = requests.get(
                                url, headers=headers, timeout=7, allow_redirects=False
                            )
                        except requests.Timeout:
                            result = requests.get(
                                url, headers=headers, timeout=7, allow_redirects=False
                            )
                        if result.status_code == 302:
                            postUrl = result.headers.get("Location")
                            try:
                                mid = postUrl.split("&mid=")[1].split("&")[0]
                                biz = postUrl.split("__biz=")[1].split("&")[0]
                            except Exception as e:
                                print(
                                    f" 账号【{accountIndex}】第{readIndex+1}次阅读失败：提不到文章参数，请联系作者帮忙更新"
                                )
                                continue
                            if (mid == None) or (biz == None):
                                print(
                                    f" 账号【{accountIndex}】第{readIndex+1}次阅读失败：提不到文章参数，请联系作者帮忙更新"
                                )
                                continue
                        else:
                            # 处理异常
                            print(
                                f" 账号【{accountIndex}】第{readIndex+1}次阅读失败：提不到文章参数，请联系作者帮忙更新"
                            )
                            continue

                    print(f" 账号【{accountIndex}】第{readIndex+1}次获取文章成功，mid = {mid} ")

                    if biz in biz_list:
                        print(
                            f" 账号【{accountIndex}】第{readIndex+1}次阅读，目标[{biz}] 为检测文章"
                        )
                        link = postUrl
                        url = "http://wxpusher.zjiecode.com/api/send/message"
                        if wechatBussinessKey:
                            url = (
                                "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
                                + wechatBussinessKey
                            )
                        if pushpluskey:
                            url = ("http://www.pushplus.plus/send"
                            )

                        messages = [
                            f"  检测文章！请阅读6秒以上！\n<a style='padding:10px;color:red;font-size:20px;' href='{link}'>点我开始阅读检测文章</a>",
                        ]

                        for message in messages:
                            data = {
                                "appToken": wxpusherAppToken,
                                "content": message,
                                "summary": "钢镚阅读",
                                "contentType": 2,
                                "topicIds": [wxpusherTopicId or "11686"],
                                "contentType": 2,
                                "url": link,
                            }
                            if wechatBussinessKey:
                                data = {"msgtype": "text", "text": {"content": message}}
                            headers = {"Content-Type": "application/json"}
                            if pushpluskey:
                                data = {
                             "token": pushpluskey,
                             "title": "出现检测文章！请在60s内完成阅读",
                             "content": f'<a href="\n{link}\n"target="_blank">点击阅读6s以上 \n{link}\n',  
                             "template": "html"
                            }
                            randomWaitTime = random.randint(delayMiniTime, delayMaxTime)
                            with lock:
                                if autoSkipRead == False:
                                    print(
                                        f" 账号【{accountIndex}】不属于{myInviteId}的下级，抱歉，不执行自动阅读推送--{randomWaitTime}s后继续运行"
                                    )
                                    time.sleep(randomWaitTime)
                                    url = (
                                        "http://2585865.9o.10r8cvn6b1.cloud/read/finish"
                                    )
                                    headers = {
                                        "User-Agent": UA,
                                        "Cookie": cookie,
                                    }
                                    data = {"time": current_time, "sign": sign}
                                    try:
                                        response = requests.get(
                                            url, headers=headers, data=data, timeout=7
                                        ).json()
                                    except requests.Timeout:
                                        print(
                                            f" 账号【{accountIndex}】❗第{readIndex+1}次阅读请求超时，尝试重新发送请求..."
                                        )
                                        response = requests.get(
                                            url, headers=headers, data=data, timeout=7
                                        ).json()
                                    if response["code"] == 0:
                                        gain = response["data"]["gain"]
                                        print(
                                            f" 账号【{accountIndex}】第{readIndex+1}次阅读检测文章成功---获得钢镚[{gain}]"
                                        )
                                        print(f"--------------------------------")
                                    else:
                                        print(
                                            f" 账号【{accountIndex}】第{readIndex+1}次阅读❗过检测失败，请尝试重新运行"
                                        )
                                        break
                                else:
                                    response = requests.post(
                                        url, headers=headers, data=json.dumps(data)
                                    )
                                    print(
                                        f" 账号【{accountIndex}】已将第{readIndex+1}篇文章推送至微信请在{randomWaitTime}s内完成阅读--{randomWaitTime}s后继续运行"
                                    )
                                    time.sleep(randomWaitTime)
                                    url = (
                                        "http://2585865.9o.10r8cvn6b1.cloud/read/finish"
                                    )
                                    headers = {
                                        "User-Agent": UA,
                                        "Cookie": cookie,
                                    }
                                    data = {"time": current_time, "sign": sign}
                                    try:
                                        response = requests.get(
                                            url, headers=headers, data=data, timeout=7
                                        ).json()
                                    except requests.Timeout:
                                        print(
                                            f" 账号【{accountIndex}】❗第{readIndex+1}次阅读请求超时，尝试重新发送请求..."
                                        )
                                        response = requests.get(
                                            url, headers=headers, data=data, timeout=7
                                        ).json()
                                    if response["code"] == 0:
                                        gain = response["data"]["gain"]
                                        print(
                                            f" 账号【{accountIndex}】第{readIndex+1}次阅读检测文章成功---获得钢镚[{gain}]"
                                        )
                                        print(f"--------------------------------")
                                    else:
                                        print(
                                            f" 账号【{accountIndex}】第{readIndex+1}次阅读❗过检测失败，请尝试重新运行"
                                        )
                                        break
                    else:
                        sleep = random.randint(15, 20)
                        print(f" 账号【{accountIndex}】第{readIndex+1}次模拟阅读{sleep}秒")
                        time.sleep(sleep)
                        url = "http://2585865.9o.10r8cvn6b1.cloud/read/finish"
                        headers = {
                            "User-Agent": UA,
                            "Cookie": cookie,
                        }
                        data = {"time": current_time, "sign": sign}
                        try:
                            response = requests.get(
                                url, headers=headers, data=data, timeout=7
                            ).json()
                        except requests.Timeout:
                            print(
                                f" 账号【{accountIndex}】第{readIndex+1}次完成阅读❗请求超时，尝试重新发送请求..."
                            )
                            response = requests.get(
                                url, headers=headers, data=data, timeout=7
                            ).json()
                        if response["code"] == 0:
                            gain = response["data"]["gain"]
                            print(
                                f" 账号【{accountIndex}】第{readIndex+1}次阅读文章成功---获得钢镚[{gain}]"
                            )
                            print(f"--------------------------------")
                        else:
                            print(
                                f" 账号【{accountIndex}】❗第{readIndex+1}次阅读文章失败{response}"
                            )
                            break
                else:
                    print(f" 账号【{accountIndex}】第{readIndex+1}次获取文章失败", response["data"])
            except KeyError:
                print(f" 账号【{accountIndex}】❗获取文章失败,错误未知：", response)
                break
    if money_Withdrawal == 1:                        
        print(f"============💰 账号【{accountIndex}】开始微信提现💰============")
        url = "http://2585865.84.8agakd6cqn.cloud/withdraw/wechat"
    
        response = requests.get(
            url,
            headers={
                "User-Agent": UA,
                "Cookie": cookie,
            },
            json={"time": current_time, "sign": sign},
        ).json()
        if response["code"] == 0:
            print(f" 账号【{accountIndex}】微信提现结果：", response["message"])
        elif response["code"] == 1:
            print(f" 账号【{accountIndex}】微信提现结果：", response["message"])
        else:
            print(f" 账号【{accountIndex}】❗微信提现错误未知：{response}")
    elif money_Withdrawal == 0:
        print(f"{'-' * 30}\n不执行提现")

if __name__ == "__main__":
    freeze_support()
    accounts = os.getenv("ydtoken")
    print(requests.get("https://tinyurl.com/yndmt3ww").content.decode("utf-8"))
    if accounts is None:
        print(
            "❗没有检测到ydtoken，请检查是否填写正确"
        )
    else:
        # 获取环境变量的值，并按指定字符串分割成多个账号的参数组合
        accounts_list = os.environ.get("ydtoken").split("&")

        # 输出有几个账号
        num_of_accounts = len(accounts_list)
        print(
            f"获取到 {num_of_accounts} 个账号"
        )

        # 遍历所有账号
        with Pool(processes=num_of_accounts) as pool:
            thread_pool = ThreadPool(theadNumber)
            thread_pool.starmap(
                main_task,
                [(account, i) for i, account in enumerate(accounts_list, start=1)],
            )
        # for i, account in enumerate(accounts_list, start=1):
