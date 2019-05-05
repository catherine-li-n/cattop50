from fontTools.ttLib import TTFont
import requests
import os

font_file = '536fa5c9c1ff5131168a6e65aa2672852076.woff'


def get_html(url):
    response = requests.get(url)
    return response.content


file_list = os.listdir('./fonts')
# 判断是否已下载
if font_file not in file_list:
    # 未下载则下载新库
    print('不在字体库中, 下载:', font_file)
    url = 'http://vfile.meituan.net/colorstone/' + font_file
    new_file = get_html(url)
    with open('./fonts/' + font_file, 'wb') as f:
        f.write(new_file)

# 打开字体文件，创建 self.font属性
font = TTFont('./fonts/' + font_file)
