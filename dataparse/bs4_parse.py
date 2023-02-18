"""
    需要安装: beautifulesoup4 和 lxml
    BeautifulSoup数据解析原理:
    -- 通过实例化一个BeautifulSoup对象,并且将页面源码数据加载到对象中
    -- 通过调用BeautifulSoup对象中相关的属性或者方法进行标签定位和数据提取
"""
import requests

"""
    BeautifulSoup用法
    -- soup.tagName         bs中第一次出现的标签内容
    -- soup.find('div')     相当于soup.div
    -- soup.find('div', class_='song')  soup.find基于属性定位
    -- soup.find_all()      找出符合要求的所有标签
    -- soup.select
        -- soup.select('某种选择器(id,class,标签..选择器)') 返回的是一个列表
        -- soup.select('.class > ul > li > a') 返回最后层级的一个列表，
                                                '>' 表示的是一个层级 ' '表示的多个层级
          -- 获取标签中的文本数据
            -- soup.tagName 标签获取标签中的文本内容有三种方法: string/text/get_text()
                            其中text/get_text() 可以获取非直系的文本内容
                            string 获取到的是标签直系的文本内容 
         -- 获取标签中的属性值
            
"""

from bs4 import BeautifulSoup

def build_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 ',
    }
    return headers



def test_beautiful_soup():
    file_name = 'test_bs.html'
    fp = open(file_name, 'r', encoding='utf-8')
    # 或者使用
    # page_text = response.text
    # BeautifulSoup(page_text, 'lxml') 直接构建BS
    soup = BeautifulSoup(fp, 'lxml')
    print(soup.a.text)
    # print(soup.find('div', class_='tang'))
    print(soup.find_all('p'))
    # select 选择器，'.tang' 相当于 class=tang
    # print(soup.select('.tang'))
    print(soup.select('.tang > ul > li > a')[0])
    print(soup.select('.tang > ul a')[1])
    # print(soup.select('.song > p')[0].text)
    # print(soup.select('.song > p')[1].string)
    print(soup.find('div', class_='song').get_text())
    print(soup.select('.tang > ul > li > a')[0]['href'])


"""
    爬取三国演义小说中所有的章节标题和章节内容
"""


def ThreeKingdom():
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    headers = build_headers()
    page_text = requests.get(url=url, headers=headers).content.decode('utf-8')

    soup = BeautifulSoup(page_text, 'lxml')
    chap_list = soup.select('.book-mulu > ul > li > a')[:]

    filename = './sanguo.txt'
    fp = open(filename, 'w', encoding='utf-8')
    for a_tag in chap_list:
        title = a_tag.text
        detail_url = 'https://www.shicimingju.com' + a_tag['href']
        chap_detail = requests.get(url=detail_url, headers=headers).content.decode('utf-8')
        detail_soup = BeautifulSoup(chap_detail, 'lxml')
        detail = detail_soup.find('div', class_='chapter_content')
        fp.write(title)
        fp.write(detail.text)
    fp.close()


if __name__ == "__main__":
    # test_beautiful_soup()
    ThreeKingdom()