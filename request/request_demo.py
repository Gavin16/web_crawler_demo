import json

"""
    requests 模块在网络爬虫中主要用于网络请求
    
"""


import requests

sg_url = "https://www.sogou.com/"


def getSogou():
    resp = requests.get(url=sg_url)
    text = resp.text
    print(text)
    with open('./sogou.html', 'w', encoding='utf-8') as fp:
        fp.write(text)

    print("爬取数据结束！")


'''
UA检测: UserAgent 请求载体的身份标识
        服务器会检测对应请求的载体身份标识,如果检测到请求的载体身份标识为某一款浏览器
        说明该请求时一个正常请求。 但是如果检测到请求的载体身份标识不是一个基于某一浏览器
        则可能会请求失败。
反爬虫策略: UA伪装
'''


def build_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 ',
    }
    return headers


def searchSogou():
    url = sg_url + 'web'
    kw = input(' enter a keyword: ')
    param = dict()
    param['query'] = kw

    headers = build_headers()

    response = requests.get(url=url, params=param, headers=headers)
    resp_text = response.text
    filename = kw + '.html'
    with open(filename, 'w', encoding='utf-8') as fd:
        fd.write(resp_text)
    print(filename, '保存成功！')


def baiduFanYi():
    url = 'https://fanyi.baidu.com/sug'
    keyword = input('enter translate sentence:')
    data = {
        'kw': keyword
    }
    headers = build_headers()
    response = requests.post(url=url, data=data, headers=headers)
    # 确认响应数据是json使用json
    json = response.json()
    print(json)
    filename = keyword + '.json'
    with open(filename, 'w', encoding='utf-8') as fd:
        fd.write(json)
    print(filename, '翻译数据保存成功!')


def buildDBMovieRankParam(start: int, count: int, ):
    param = {
        'start': start,
        'limit': count,
        'action': '',
        'type': '24',
        'interval_id': '100:90'
    }
    return param


def douBanMovieRank():
    url = 'https://movie.douban.com/j/chart/top_list'
    headers = build_headers()
    param = buildDBMovieRankParam(0, 100)
    response = requests.get(url=url, headers=headers, params=param)
    status_code = response.status_code
    if status_code == 200:
        list_data = response.json()
        filename = '豆瓣喜剧top100.txt'
        fd = open(filename, 'w', encoding='utf-8')
        for record in list_data:
            rank = '豆瓣排名: ' + str(record["rank"])
            title = '电影名称: ' + record["title"]
            release_date = '上映时间: ' + record["release_date"]
            score = '豆瓣评分: ' + record["score"]
            region = '上映地区: ' + record["regions"][0]
            fd.write(rank + '\n')
            fd.write(title + '\n')
            fd.write(release_date + '\n')
            fd.write(region + '\n')
            fd.write(score + '\n')
            sub_list = record["actors"][0:4]
            main_actors = ', '.join(sub_list)
            fd.write("主演演员: " + main_actors + '\n\n')
        fd.flush()
        fd.close()
    else:
        print('接口请求失败:', response.status_code, response.content)


def KFCShopSites():
    url = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    heads = build_headers()
    params = {
        'cname':'',
        'pid':'',
        'keyword': '深圳',
        'pageIndex': 1,
        'pageSize': 300
    }
    response = requests.post(url=url, headers=heads, params=params)
    resp_text = response.text
    filename = 'KFCShopSite.txt'
    with open(filename, 'w', encoding='utf-8') as fd:
        fd.write(resp_text)
    print(filename, '地址信息保存成功!')


"""
    初始页面不包含,需要动态加载才能获得的数据
    
"""


def DynamicLoadedDate():
    pass


if __name__ == "__main__":
    # searchSogou()
    # baiduFanYi()
    douBanMovieRank()
    # KFCShopSites()