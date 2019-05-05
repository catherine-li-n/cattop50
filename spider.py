# -*-coding:utf-8-*-
import json
import re
import os
import requests
from fontTools.ttLib import TTFont
from requests import RequestException
from multiprocessing import Pool
rootdir = './fonts/'
font = None
font_file = ''


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def get_html(url):
    response = requests.get(url)
    return response.content


def check_font():
    global font
    file_list = os.listdir('./fonts')
    if font_file not in file_list:
        print('不在字体库中, 下载:', font_file)
        url = 'http://vfile.meituan.net/colorstone/' + font_file
        new_file = get_html(url)
        with open('./fonts/' + font_file, 'wb') as f:
            f.write(new_file)
    font = TTFont(rootdir + font_file)


def trans2num(ss):
    """&#xf613;&#xf613;&#xe57d;&#xe57d;&#xf469;"""
    font = TTFont(rootdir + font_file)
    gly_list = font.getGlyphOrder()
    gly_list = gly_list[2:]
    for number, gly in enumerate(gly_list):
        gly = gly.replace('uni', '&#x').lower() + ';'
        if gly in ss:
            ss = ss.replace(gly, str(number))
    return ss


def parse_one_page(html):
    global font_file
    font_file = re.findall(r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', html)[0]
    check_font()
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?'
                         '>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         '.*?month-wish">.*?stonefont">(.*?)</span></span>.*?total-wish">.*?stonefont">(.*?)'
                         '</span></span>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index': item[0],
            'src': item[1],
            'title': item[2],
            'cast': item[3],
            'releasetime': item[4],
            'month-wish': trans2num(str(item[5])),
            'total-wish': trans2num(str(item[6]))
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://maoyan.com/board/6?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*10 for i in range(5)])