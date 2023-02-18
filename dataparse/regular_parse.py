"""
    聚焦爬虫解析数据有如下三种方式
        (1) 正则匹配
        (2) bs4 解析
        (3) xpath解析 (重点:通用性强)
"""

"""
    编码流程:
       -- 制定URL
       -- 发起请求
       -- 获取响应数据
       -- 数据解析
       -- 持久化存储
"""
import requests
import re
import os


def build_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 ',
    }
    return headers


def GetImageDate():
    url = "https://inews.gtimg.com/newsapp_bt/0/15573068180/1000"
    headers = build_headers()
    img_data = requests.get(url=url, headers=headers).content

    with open('./image.jpg', 'wb') as fp:
        fp.write(img_data)


"""
<div class="cover">
  <a href="https://book.douban.com/subject/36085061/?icn=index-latestbook-subject" title="法国知识分子的终结？">
    <img src="https://img1.doubanio.com/view/subject/s/public/s34369807.jpg" alt="法国知识分子的终结？">
  </a>
</div>
"""


def douban_image_batch():
    url = "https://book.douban.com"
    headers = build_headers()
    page_text = requests.get(url=url, headers=headers).text
    ex = '<div class="cover">\s* <a href="(.*?)" title="(.*?)">\s*<img src="(.*?)" alt="(.*?)">\s*</a>\s*</div>'
    img_src_list = re.findall(ex, page_text, re.M)
    if not os.path.exists('./douban_book'):
        os.mkdir('./douban_book')
    for img_src in img_src_list:
        img_url = str(img_src[2])

        img_data = requests.get(url=img_url, headers=headers).content

        img_name = img_url.split('/')[-1]
        img_path = './douban_book/' + img_name
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
    print('所有图片下载成功！')


if __name__ == "__main__":
    douban_image_batch()

