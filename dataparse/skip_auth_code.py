"""
    需要登录网站跳过验证码

"""
import requests
from lxml import etree
import ddddocr


def build_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    return headers


"""
    通过验证码地址获取图片,并保存在本地
    返回验证码文件本地存储地址
"""


def save_code_img(image_url: str):
    code_path = './code.jpg'
    img_data = requests.get(url=image_url, headers=headers).content
    with open(code_path, 'wb') as fd:
        fd.write(img_data)
    return code_path


"""
    ddddocr 识别验证码    
"""


def img_code_ocr(image_path: str):
    ocr = ddddocr.DdddOcr()
    with open(image_path, 'rb') as fd:
        img_bytes = fd.read()
    code = ocr.classification(img_bytes)
    return code


if __name__ == "__main__":
    url = "https://so.gushiwen.cn/user/login.aspx"
    url_home = 'https://so.gushiwen.cn'
    headers = build_headers()
    page_text = requests.get(url=url, headers=headers).text

    tree = etree.HTML(page_text)
    img_src = tree.xpath('//*[@id="imgCode"]/@src')[0]
    img_url = url_home + img_src
    img_path = save_code_img(img_url)
    # 调用ddddocr识别验证码
    res = img_code_ocr(img_path)
