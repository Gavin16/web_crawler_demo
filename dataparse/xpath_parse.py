"""
    需要安装: lxml (pip安装即可)
    xpath 不仅可以应用到python 中，还能应用到其它语言: JavaScript、Java、PHP、Python、C、C++等

    xpath 解析原理:
        -- 实例化一个etree的对象, 且要将被解析的页面源码数据加载到该对象中
        -- 调用etree对象中的xpath 方法结合着xpath 表达式实现标签的定位和内容的捕获
    etree对象实例化:
        -- 1. 将本地读取的html文档中的源码数据加载到etree对象中
                etree.parse(filePath)
        -- 2. 可以将互联网上获取的源码数据加载到该对象中
                etree.HTML('page_text')
        -- 3. 调用etree.xpath方法，方法传参指定xpath表达式

    xpath表达式:
        1. / 代表从根节点开始定位, 一个'/' 表示一个层级，
        2. // 表示的是多个层级, 可以表示从任意位置开始定位
        3. 属性定位: //div[@class="song"]
        4. 索引定位: /html//div[@class='song']/p[2]; 索引是从1开始的
        5. 取文本:
              -- /text() 获取的是标签中直系的文本内容
              -- //text() 获取的是非直系的文本内容(所有文本内容)
        6. 取属性:
              -- /@attrName: 取某个标签下attrName属性的属性值
        7. 逻辑运算符:
              -- 逻辑或 '|'
                 如: //div[@class="bottom"]/ul/li | //div[@class="bottom"]/ul/div[2]/li
                 可以返回两个xpath表达式的数据并集
"""

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
from lxml import etree

# HTTPS 跳过验证警告信息关闭
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
    解析xpath 表达式
"""


def xpath_express():
    tree = etree.parse('test_xpath.html')
    # res = tree.xpath('/html/head/title')
    # res = tree.xpath('//div')
    # res = tree.xpath('//div[@class="song"]/p[4]')
    print(tree.xpath('//div[@class="tang"]//li[4]/a/text()')[0])
    print(tree.xpath('//li[6]//text()')[0])
    print(tree.xpath('//div[@class="tang"]//text()'))
    print(tree.xpath('//div[@class="song"]/img/@src'))


def build_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    return headers


"""
    获取58上二手房信息    
"""


def second_hand_house():
    url = "https://www.58.com/ershoufang/"
    headers = build_headers()
    page_text = requests.get(url=url, headers=headers).text
    # 数据解析
    tree = etree.HTML(page_text)
    tr_list = tree.xpath('//table[@class="tbimg"]/tr')

    image_path = './house_image'
    if not os.path.exists(image_path):
        os.mkdir(image_path)

    house_info_file = './58.txt'
    fd0 = open(house_info_file, 'w', encoding='utf-8')
    for tr in tr_list:
        td = tr.xpath('./td')[1]
        text_list = td.xpath('.//text()')
        # print(str(text_list))
        for info in text_list:
            fd0.write(info + '\n')
        fd0.write('\n')
        # print(src)
        # image_url = 'https:' + src
        # image_data = requests.get(url=image_url, headers=headers).content
        #
        # filename = src.split('/')[-1]
        # img_file_path = image_path + '/' + filename
        # with open(img_file_path, 'wb') as fd1:
        #     fd1.write(image_data)
    fd0.close()


def high_clear_mn_pic():
    page_home = 'https://pic.netbian.com'
    url = 'https://pic.netbian.com/4kmeinv/'
    headers = build_headers()
    page_text = requests.get(url=url, headers=headers).content.decode('gbk')
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//div[@class="slist"]/ul[@class="clearfix"]/li')

    hd_pic_path = './4k_image'
    if not os.path.exists(hd_pic_path):
        os.mkdir(hd_pic_path)

    for li in li_list:
        img_src = li.xpath('./a/img/@src')[0]
        img_url = page_home + img_src
        img_data = requests.get(url=img_url, headers=headers).content
        img_name = img_url.split('/')[-1]
        img_path = hd_pic_path + '/' + img_name
        with open(img_path, 'wb') as fd:
            fd.write(img_data)
    print("4K高清图片保存成功")


def find_all_cities():
    url = 'https://www.aqistudy.cn/historydata/'
    headers = build_headers()
    # /aqistudy网址证书过期,
    page_text = requests.get(url=url, headers=headers, verify=False).text
    tree = etree.HTML(page_text)

    li_list = tree.xpath('//div[@class="all"]/div[@class="bottom"]/ul/div[2]/li')
    city_name_list = list()
    for li in li_list:
        city_name = li.xpath('./a/text()')[0]
        city_name_list.append(city_name)

    print("所有城市一共:", len(city_name_list))
    print(city_name_list)

    # 一次性获取所有 热门城市+所有城市的城市名
    # 热门城市层级关系: '//div[@class="bottom"]/ul/li/a'
    # 所有城市层级关系: '//div[@class="bottom"]/ul/div[2]/li/a'
    hot_and_all_list = list()
    m_tree = etree.HTML(page_text)
    big_li_list = m_tree.xpath('//div[@class="bottom"]/ul/li | //div[@class="bottom"]/ul/div[2]/li')
    for li in big_li_list:
        city_name = li.xpath('./a/text()')[0]
        hot_and_all_list.append(city_name)
    print("热门+所有城市一共:", len(hot_and_all_list))
    print(hot_and_all_list)


if __name__ == "__main__":
    # xpath_express()
    # second_hand_house()
    # high_clear_mn_pic()
    find_all_cities()