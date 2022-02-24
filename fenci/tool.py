import datetime
import requests
import json
import re


# 获取当前时间
def getTime():
    month = datetime.datetime.today().month
    if 3 <= month <= 5 or 9 <= month <= 11:
        return 2
    if 6 <= month <= 8:
        return 1
    else:
        return 3


# 获取当前气温
def getTemperature():
    rb = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=上海')
    data = json.loads(rb.text)
    t = data['data']['forecast'][0]['high']
    temperature = int(re.findall(r" (.+?)℃", t)[0])
    if 10 <= temperature <= 20:
        return 2
    if temperature < 10:
        return 3
    if temperature > 20:
        return 1


# 获取场景
def getScene(scene):
    if scene == '职场':
        return 1
    if scene == '休闲':
        return 2
    if scene == '聚会':
        return 3
    else:
        return 4


if __name__ == '__main__':
    print(getTime())
    print(getTemperature())
