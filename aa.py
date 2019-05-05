from fontTools.ttLib import TTFont
ss = '&#xf613;&#xf613;&#xe57d;&#xe57d;&#xf469;'
rootdir = './fonts/'
font_file = '536fa5c9c1ff5131168a6e65aa2672852076.woff'
font = TTFont(rootdir+font_file)
gly_list = font.getGlyphOrder()     # 获取 GlyphOrder 字段的值
for number, gly in enumerate(gly_list):
    # 把 gly 改成网页中的格式
    print(gly)
    gly = gly.replace('uni', '&#x').lower() + ';'
    # 如果 gly 在字符串中，用对应数字替换
    if gly in ss:
        ss = ss.replace(gly, str(number))
# 返回替换后的字符串
print(ss)
