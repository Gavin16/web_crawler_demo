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


def build_zhihu_header():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 ',
        'cookie': 'q_c1=0de9b91594954aeb836120aa24e30c33|1671770029000|1671770029000; '
                  '_zap=796161a0-d3c9-44d0-91c4-8b78f4455a0f; d_c0=AMBWEDhkDxaPTiy56JavpBtts16GUtpF4sQ=|1671770026; '
                  'YD00517437729195%3AWM_TID=0DGDFQ2cNctAEUERUBaRdwqnNUg0PEw8; __snaker__id=jqVqjIxtdu76ThHy; '
                  'YD00517437729195%3AWM_NI=Z3KgdGktQImhb%2F1Svcb2R08UQnTuFS8M1ho2F57d4ha2SLameTuAhTT5yb1At0'
                  '%2Fp8QED2WB91oR4awJrgImWM%2BJ3CD7nrKxZyKzIIAYGO8wmiCcqrjHp%2B5IJGgH%2BzidPdU8%3D; '
                  'YD00517437729195%3AWM_NIKE'
                  '=9ca17ae2e6ffcda170e2e6eebbf07cf8a8a49ae96d9c968ab6c84e939e9eacc443bb8d9fb1ae7a81f09ad3fc2af0fea7c3b92a9aed8588e74da9ac9faaf064a2f1ffb4f569a2ee9ed1bb5f93b29c96c559fc93ff89ee3a86ebf985b764a3ee9dade467a78cbba2eb6098ebb783b44bb8f0e191bb5b879cfeb8c133f3b19ed5e47d8aaea9aaf05d8ff586d4c250f5b2beacfb52bb95b6aacc4b9b9981d9f667ab9dad92f1628cb0e5d6cc4285b988ccf963a890acb6bb37e2a3; q_c1=379c559d0589412e9abad1cf0affdeff|1671958646000|1671958646000; _xsrf=3b3b52c5-cf5d-45b9-a31f-c085aff03d6c; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1676473638; arialoadData=false; z_c0=2|1:0|10:1676515269|4:z_c0|80:MS4xY0hJVEFBQUFBQUFtQUFBQVlBSlZUVEhUd0dUZFpDbFd5NkpGU0pjdV9IRU9VWnhKSjZubzlRPT0=|5e28c714c3cd080801f2e0a14c97bb1116ec7a957864e3c8f2192285e5ed7b00; SESSIONID=8bg2vwpiOSbWhPXd7n43CZgoroAqYOk0QKvtnRT2RmJ; JOID=VlERA06AS-FBAoUCJYT3ubkX-lsztSSCdnX_f0jOFY4Sb9RXTIuLDSYOhQskcjASoo76Rby3IBKGfoeBftw0CYE=; osd=U1kSBk6FQ-JEAoAKJoH3vLEU_1s2vSeHdnD3fE3OEIYRatRSRIiODSMGhg4kdzgRp47_Tb-yIBeOfYKBe9Q3DIE=; BAIDU_SSP_lcr=https://cn.bing.com/; KLBRSID=3d7feb8a094c905a519e532f6843365f|1676527891|1676527880; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1676527893; tst=r '
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
    # GetImageDate()
