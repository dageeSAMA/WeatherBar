import os
import signal

import requests
from flask import Flask, render_template, request, after_this_request
from lxml import etree
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    location = '122.54,42.37'
    specify_location = request.args.get('location', type=str)
    if specify_location is not None:
        location = specify_location
    # 彰武坐标  '122.54,42.37'
    # '101282101'
    # 使用api获取数据

    key = '5c00cf403a6b46d4b2f5f6ea984ea8d4'
    # 使用api查询位置坐标静态页
    response_for_lookup = requests.get(
        'https://geoapi.qweather.com/v2/city/lookup?key=' + key + '&location=' + location)
    # 使用api查询当前天气
    response_for_now = requests.get('https://devapi.qweather.com/v7/weather/now?key=' + key + '&location=' + location)

    # 使用api查询24h天气
    response_for_24h = requests.get('https://devapi.qweather.com/v7/weather/24h?key=' + key + '&location=' + location)
    # 使用api查询3天预报
    response_for_3days = requests.get('https://devapi.qweather.com/v7/weather/3d?key=' + key + '&location=' + location)
    # 使用api查询预警
    response_for_warning = requests.get(
        'https://devapi.qweather.com/v7/warning/now?key=' + key + '&location=' + location)
    data_lookup = response_for_lookup.json()
    if data_lookup['code'] != '200':
        return "<h1>位置代码或信息输入错误</h1>"
    url = data_lookup['location'][0]['fxLink']

    # url = 'https://www.qweather.com/weather/zhangwu-101070902.html'
    # 向url进行requests
    response = requests.get(url)
    html_content = response.text
    html_tree = etree.HTML(html_content)
    # 获（tou）取当天天气情况描述
    today_weather_text = html_tree.xpath('/html/body/div[3]/div[3]/div/div[1]/div/div/div[2]/text()')[0]
    #
    # 获（tou）取当前天空颜色和背景图
    current_weather_bg_steal = html_tree.xpath('/html/body/div[3]/div[3]/div/div[1]/div')
    for element in current_weather_bg_steal:
        # 获取背景所在元素的类名
        current_weather_bg_class = element.attrib.get('class')

    data_now = response_for_now.json()
    data_24h = response_for_24h.json()
    data_3days = response_for_3days.json()
    data_warning = response_for_warning.json()

    # 传参
    def check_time_period():
        # 获取当前日期
        today_date = datetime.now().date()

        # 设定日出和日落时间
        sunrise_time = datetime.combine(today_date, datetime.strptime(data_3days['daily'][0]['sunrise'], "%H:%M").time())
        sunset_time = datetime.combine(today_date, datetime.strptime(data_3days['daily'][0]['sunset'], "%H:%M").time())

        # 获取当前时间
        current_time = datetime.now()

        # 比较当前时间与日出时间和日落时间
        if current_time < sunrise_time:
            return "dark"
        elif sunrise_time <= current_time <= sunset_time:
            return "light"
        else:
            return "dark"

    data = {
        'theme': check_time_period(),
        'today_weather_text': today_weather_text,
        'current_weather_bg_class': current_weather_bg_class,
        'location_name': data_lookup['location'][0]['name'],
        'now_icon': data_now['now']['icon'],
        'now_weather': data_now['now']['text'],
        'now_temp': data_now['now']['temp'],
        'today_lowest_temp': data_3days['daily'][0]['tempMin'],
        'today_highest_temp': data_3days['daily'][0]['tempMax'],
        'sunrise_time': data_3days['daily'][0]['sunrise'],
        'sunset_time': data_3days['daily'][0]['sunset'],
        'a1h_temp': data_24h['hourly'][0]['temp'],
        'a3h_temp': data_24h['hourly'][2]['temp'],
        'a5h_temp': data_24h['hourly'][4]['temp'],
        'a7h_temp': data_24h['hourly'][6]['temp'],
        'a9h_temp': data_24h['hourly'][8]['temp'],
        'a11h_temp': data_24h['hourly'][10]['temp'],
        'a13h_temp': data_24h['hourly'][12]['temp'],
        'a1h_icon': data_24h['hourly'][0]['icon'],
        'a3h_icon': data_24h['hourly'][2]['icon'],
        'a5h_icon': data_24h['hourly'][4]['icon'],
        'a7h_icon': data_24h['hourly'][6]['icon'],
        'a9h_icon': data_24h['hourly'][8]['icon'],
        'a11h_icon': data_24h['hourly'][10]['icon'],
        'a13h_icon': data_24h['hourly'][12]['icon'],
        'a1h_precip': data_24h['hourly'][0]['precip'],
        'a3h_precip': data_24h['hourly'][2]['precip'],
        'a5h_precip': data_24h['hourly'][4]['precip'],
        'a7h_precip': data_24h['hourly'][6]['precip'],
        'a9h_precip': data_24h['hourly'][8]['precip'],
        'a11h_precip': data_24h['hourly'][10]['precip'],
        'a13h_precip': data_24h['hourly'][12]['precip'],

    }

    check_time_period()
    if len(data_warning['warning']) == 0:
        weather_warnings = {
            'warning_exist': 0
        }
    else:
        severity_color = data_warning['warning'][0]['severityColor']
        if severity_color == "White":
            severity_color = "rgba(255, 255, 255, 0.5)"
        elif severity_color == "Blue":
            severity_color = "rgba(100, 100, 255, 0.5)"
        elif severity_color == "Green":
            severity_color = "rgba(100, 255, 100, 0.5)"
        elif severity_color == "Yellow":
            severity_color = "rgba(255, 255, 100, 0.5)"
        elif severity_color == "Orange":
            severity_color = "rgba(255, 128, 100, 0.5)"
        elif severity_color == "Red":
            severity_color = "rgba(255, 100, 100, 0.5)"
        elif severity_color == "Black":
            severity_color = "rgba(0, 0, 0, 0)"

        weather_warnings = {
            'warning_exist': 1,
            'severity_color': severity_color,
            'level': data_warning['warning'][0]['level'],
            'type': data_warning['warning'][0]['type'],
            'type_name': data_warning['warning'][0]['typeName']

        }
    return render_template("index.html", data=data, weather_warnings=weather_warnings)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    # curl -X POST localhost:5000/shutdown


if __name__ == '__main__':
    app.run(debug=True)
