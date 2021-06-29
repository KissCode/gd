"""
宠汪汪兑换Pro
更新时间：2021-06-30

在Line 63设置cookie
cookies = ['ck1','ck2','ck3']
或环境变量JD_COOKIE以&分割
export JOYPRO_JD_COOKIE="ck1&ck2&ck3"

cron 59 7,15,23 * * * * 或 0 0,8,16 * * *
"""

import json
import os
import sys
import threading
import time
import datetime
	@@ -42,30 +43,26 @@ def main(cookie, validate):
        config = tasks['data']['beanConfigs16']

    for bean in config:
        sys.stdout.write(f"{bean['id']} {bean['giftName']} {bean['leftStock']}\n")
        if bean['giftValue'] == target:
            while 1:
                if datetime.datetime.now().second == 0:
                    break
                time.sleep(0.1)
            sys.stdout.write('exchange()\n')
            url = f"https://jdjoy.jd.com/common/gift/new/exchange?reqSource=h5&invokeKey=NRp8OPxZMFXmGkaE&validate={validate}"
            data = {"buyParam": {"orderSource": 'pet', "saleInfoId": bean['id']}, "deviceInfo": {}}
            res = requests.post(url, headers=headers, data=json.dumps(data)).json()
            sys.stdout.write(json.dumps(res) + '\n')
            if res['errorCode'] == 'buy_success':
                sys.stdout.write(f"cookie{cookie.split('pt_pin=')[1].replace(';', '')}兑换成功\n")
    lock.release()


if __name__ == '__main__':
    print("🔔宠汪汪兑换Pro,开始！")
    # cookies = ['ck1','ck2','ck3']
    cookies = []
    if os.environ.get("JOYPRO_JD_COOKIE"):
        cookies.append(os.environ.get("JOYPRO_JD_COOKIE").split('&'))
    lock = threading.BoundedSemaphore(20)
    if 'test' in os.getcwd():
        path = '..'
    else:
        path = '.'
    with open(f'{path}/validate.txt', encoding='utf-8') as f:
        validates = f.read().split('\n')[:-1]
    print(f"====================共{len(cookies)}个京东账号Cookie=========")
    for i in range(min(len(validates), len(cookies))):
        lock.acquire()
        threading.Thread(target=main, args=(str(cookies[i]), validates[i])).start()
