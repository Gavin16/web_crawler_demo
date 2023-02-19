"""
    使用代理服务器防止本机IP被封
    代理作用:
        -- 可以突破IP访问的限制
        -- 可以隐藏自身真实的IP
"""
import requests


def build_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 ',
    }
    return headers


if __name__ == "__main__":
    url = 'https://www.baidu.com/s?wd=ip'
    header_params = build_headers()
    proxies = {
        'https': '92.223.65.63:40430'
    }
    page_text = requests.get(url=url, headers=header_params).text

    file_path = './baidu_ip.html'
    with open(file_path, 'w', encoding='utf-8') as fp:
        fp.write(page_text)
