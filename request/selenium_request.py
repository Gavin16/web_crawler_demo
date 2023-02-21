"""
    selenium 在爬虫中的作用
    -- 1. 可以非常便捷的获取动态加载出来的数据
    -- 2. 可以便捷的实现模拟登录

    selenium 是什么?
    -- 一个基于浏览器自动化的模块，通过selenium代码可以操作浏览器

    selenium 操作流程:
    (1) pip install selenium
    (2) 下载 chrome 驱动程序
         -- 下载路径: http://chromedriver.storage.googleapis.com/index.html
         -- 驱动程序和浏览器的映射关系: 2023年之后,driver版本已经与chrome浏览器版本一致


    对于一些防爬虫机制做的好的网站,同时数据量不太大的网站,可以考虑使用selenium获取数据

"""
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree

# 实现浏览器无可视化界面
from selenium.webdriver.chrome.options import Options

# 规避网站对selenium检测
from selenium.webdriver import ChromeOptions

"""
    使用selenium 获取豆瓣读书Top250书籍信息
    -- 使用标签点击方式分页查询
"""


def parse_page_and_save(first_no, fd, tree):
    table_list = tree.xpath('//*[@id="content"]/div/div[1]/div/table')
    book_no = first_no
    for table in table_list:
        td = table.xpath('./tbody/tr/td[2]')[0]
        book_name = td.xpath('./div[1]/a/text()')[0]
        book_name = str(book_name).replace('\n', '').replace(' ', '')
        book_name = '书籍名称: ' + book_name
        basic_info = str(td.xpath('./p/text()')[0]).replace(' ', '')
        evaluate_score = '豆瓣评分: ' + td.xpath('./div[2]/span[2]/text()')[0]
        evaluate_num = str(td.xpath('./div[2]/span[3]/text()')[0])\
                        .replace('\n', '').replace('(', '').replace(')', '').replace(' ', '')

        evaluate_num = '评价人数: ' + evaluate_num
        basic_info = str(basic_info)
        basic_info = '基本信息: ' + basic_info
        fd.write("书籍编号: " + str(book_no) + '\n')
        fd.write(book_name + '\n')
        fd.write(evaluate_score + '\n')
        fd.write(evaluate_num + '\n')
        fd.write(basic_info + '\n\n')
        book_no = book_no + 1
    return book_no


def get_douban_book_top250():
    # 去掉chrome可视化界面
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 规避selenium 被检测
    # option = ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options)
    driver.get(url='https://book.douban.com/top250')

    # 图书存储文件
    filename = '豆瓣读书Top250.txt'
    fd = open(filename, 'w', encoding='utf-8')

    # 第一页数据先存储
    page_text = driver.page_source
    first_tree = etree.HTML(page_text)
    last_no = parse_page_and_save(1, fd, first_tree)

    page_selector = driver.find_element(by=By.CLASS_NAME, value="paginator")
    a_tag_list = page_selector.find_elements(by=By.TAG_NAME, value='a')

    total_page = len(a_tag_list)
    page_list = list(range(1, total_page))

    # 挨个点击第二页开始后面的每一页,并解析每一页获取到的数据
    for page_num in page_list:
        a_tag = a_tag_list[page_num]
        a_tag.click()
        page_selector = driver.find_element(by=By.CLASS_NAME, value="paginator")
        a_tag_list = page_selector.find_elements(by=By.TAG_NAME, value='a')

        page_text = driver.page_source
        tree = etree.HTML(page_text)
        # 解析文件并保存数据信息
        last_no = parse_page_and_save(last_no, fd, tree)

    fd.close()
    # 睡眠10秒结束循环
    time.sleep(10)
    driver.quit()


if __name__ == "__main__":
    get_douban_book_top250()
    # 实例化一个浏览器对象,传入驱动程序; selenium 4之后需要通过service指定传参
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.get(url='https://book.douban.com/')
    # page_text = driver.page_source
    #
    # tree = etree.HTML(page_text)
    # li_list = tree.xpath('//*[@id="content"]/div/div[1]/div[1]/div[2]/div[1]/div/ul[2]/li')
    #
    # for li in li_list:
    #     book_name = li.xpath('./div[2]/div[1]/a/text()')[0]
    #     print(book_name)
    # print("从动态加载后完整页面获取数据完成!")
    #
    # time.sleep(5)
    # driver.quit()


