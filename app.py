import requests
from flask import Flask, render_template
from lxml import etree

app = Flask(__name__)


@app.route("/")
def index():
    url = 'https://www.qweather.com/weather/zhangwu-101070902.html'
    # 彰武坐标  '122.54,42.37'
    # 深圳代码  '101280601'
    location = '122.54,42.37'
    key = '5c00cf403a6b46d4b2f5f6ea984ea8d4'
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
        # 获取元素的类名
        current_weather_bg_class = element.attrib.get('class')
        print(current_weather_bg_class)

    # 偷不到背景图
    # current_weather_bg_steal_inner = html_tree.xpath('/html/body/div[3]/div[3]/div/div[1]/div/div')
    # for element in current_weather_bg_steal_inner:
    #     # 获取元素的类名
    #     current_weather_bg_class_inner = element.attrib.get('class')
    #     print(current_weather_bg_class_inner)

    #
    # 使用api获取数据
    # 使用查询当前天气pai
    response_for_now = requests.get('https://devapi.qweather.com/v7/weather/now?key=' + key + '&location=' + location)
    # 使用查询24h天气pai
    response_for_24h = requests.get('https://devapi.qweather.com/v7/weather/24h?key=' + key + '&location=' + location)
    # 使用查询3天预报api
    response_for_3days = requests.get('https://devapi.qweather.com/v7/weather/3d?key=' + key + '&location=' + location)
    # 使用查询预警api
    response_for_warning = requests.get(
        'https://devapi.qweather.com/v7/warning/now?key=' + key + '&location=' + location)

    data_now = response_for_now.json()
    data_24h = response_for_24h.json()
    data_3days = response_for_3days.json()
    data_warning = response_for_warning.json()
    # 传参
    data = {

        'today_weather_text': today_weather_text,
        'current_weather_bg_class': current_weather_bg_class,
        # 'current_weather_bg_class_inner': current_weather_bg_class_inner,
        'now_icon': data_now['now']['icon'],
        'now_weather': data_now['now']['text'],
        'now_temp': data_now['now']['temp'],
        'today_lowest_temp': data_3days['daily'][0]['tempMin'],
        'today_highest_temp': data_3days['daily'][0]['tempMax'],
        'a2h_temp': data_24h['hourly'][1]['temp'],
        'a4h_temp': data_24h['hourly'][3]['temp'],
        'a6h_temp': data_24h['hourly'][5]['temp'],
        'a8h_temp': data_24h['hourly'][7]['temp'],
        'a10h_temp': data_24h['hourly'][9]['temp'],
        'a12h_temp': data_24h['hourly'][11]['temp'],
        'a2h_icon': data_24h['hourly'][1]['icon'],
        'a4h_icon': data_24h['hourly'][3]['icon'],
        'a6h_icon': data_24h['hourly'][5]['icon'],
        'a8h_icon': data_24h['hourly'][7]['icon'],
        'a10h_icon': data_24h['hourly'][9]['icon'],
        'a12h_icon': data_24h['hourly'][11]['precip'],
        'a2h_precip': data_24h['hourly'][1]['precip'],
        'a4h_precip': data_24h['hourly'][3]['precip'],
        'a6h_precip': data_24h['hourly'][5]['precip'],
        'a8h_precip': data_24h['hourly'][7]['precip'],
        'a10h_precip': data_24h['hourly'][9]['precip'],
        'a12h_precip': data_24h['hourly'][11]['precip'],

    }
    if len(data_warning['warning']) == 0:
        weather_warnings = {
            'warning_exist': 0
        }
    else:
        weather_warnings = {
            'warning_exist': 1,
            'severity_color': data_warning['warning'][0]['severityColor'],
            'level': data_warning['warning'][0]['level'],
            'type': data_warning['warning'][0]['type'],
            'typeName': data_warning['warning'][0]['typeName']

        }

    return render_template("index.html", data=data, weather_warnings=weather_warnings)


@app.after_request
def add_security_headers(response):
    response.headers['x-content-type-options'] = 'nosniff'
    return response


if __name__ == '__main__':
    app.run()
