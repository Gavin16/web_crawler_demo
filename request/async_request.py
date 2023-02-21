"""
    高性能异步爬虫
    目的: 在爬虫中使用异步实现高性的数据爬取操作

    异步爬虫的方式:
        --多线程:(不建议)
            有点: 可以为相关阻塞的操作单独开启线程或者进程，阻塞操作就可以异步执行
            缺点: 无法无限制的开启多线程和多进程
        --线程池:(适当使用)
            优点: 可以降低系统对进程或者线程创建或者销毁的一个频率,从而很好的降低系统的开销
            缺点: 池中线程或者进程的数量有上限
        --单线程+异步协程:(推荐)
            event_loop: 时间循环,相当于一个无线循环,我们可以把一些函数注册到这个时间循环上
                当满足某些条件的时候, 函数就会被循环执行。
            coroutine: 协程对象, 我们可以将协程对象注册到时间循环中,它会被时间循环调用
                可以使用async关键字来定义一个方法, 这个方法在调用时不会立即被执行, 而是返回
                一个协程对象
            task: 任务，他是协程对象的进一步封装,包含了任务的各个状态
            future: 代表将来执行或还没有执行的任务, 实际上和task 没有本质区别
            async: 定义一个协程
            await: 用来挂起阻塞方法的执行
"""
from multiprocessing import Pool
import asyncio
import time
import requests


def process_download(name: str):
    print("开始下载:", name)
    time.sleep(2)
    print("下载完成:", name)


def test_thread_pool():
    name_list = ["aaa", "bbb", "ddd", "ccc"]
    start_time = time.time()
    pool = Pool(4)
    # 使用map批量处理
    pool.map(process_download, name_list)

    end_time = time.time()
    print("下载耗时:", (end_time - start_time))


async def async_request(url: str):
    print("请求URL地址,", url)
    # 在异步协程中如果出现了同步模块相关的代码, 那么就无法实现异步
    # time.sleep(2)
    # 当在asyncio中遇到阻塞操作必须进行手动挂起
    await asyncio.sleep(2)
    print("请求成功,", url)
    return url


"""
        
"""


async def gather_multi(req1, req2):
    await asyncio.gather(req1, req2)


"""
    协程使用方式:
     通过loop 创建task
    (1) 调用async 关键字修饰的方法将得到一个协程对象
    (2) 创建一个时间循环对象      #asyncio.get_event_loop()
    (3) 将协程对象注册到loop中    #asyncio.create_task(c) 得到task对象
    (4) 启动loop执行任务         #asyncio.run_until_complete(task)
     通过asyncio ensure_future 创建task
    (1) 调用async 关键字修饰的方法，得到一个协程对象
    (2) 创建一个循环对象         
    (3) 通过asyncio ensure_future 创建一个task对象(将协程对象绑定到任务中)
    (4) 启动loop执行绑定任务
"""


def test_coroutine():
    url1 = "www.baidu.com"
    url2 = "www.sina.com"

    req1 = async_request("www.baidu.com")
    req2 = async_request("www.sina.com")

    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(req1)
    # task = loop.create_task(req)
    task.add_done_callback(callback_func)
    loop.run_until_complete(task)

    # 异步同时执行多个协程
    # asyncio.run(gather_multi(async_request(url1), async_request(url2)))


def callback_func(task):
    print(task.result())


def multi_request():
    start = time.time()
    urls = [
        "www.baidu.com",
        "www.sina.com",
        "www.sogou.com"
    ]
    tasks = []
    for url in urls:
        c = async_request(url)
        task = asyncio.ensure_future(c)
        tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print("multi_request执行耗时:", (time.time() - start))



async def http_request(url):
    print("请求地址:", url)
    response = requests.get(url=url)
    print("响应结果:", response.text)


"""
    使用协程 验证真实http请求 并发效果
    实际执行耗时: 6s
    因为requests 发起的请求是同步操作，因此在asyncio异步执行不再生效
"""


def real_request_test():
    urls = [
            'http://127.0.0.1:5000/bobo',
            'http://127.0.0.1:5000/mimi',
            'http://127.0.0.1:5000/jiojio'
    ]
    tasks = []
    for url in urls:
        c = http_request(url)
        task = asyncio.ensure_future(c)
        tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    # test_thread_pool()
    # test_coroutine()
    # multi_request()
    start = time.time()
    real_request_test()
    end = time.time()
    print("执行总耗时:", end - start)