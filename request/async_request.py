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
    print("请求成功,", url)
    return url

"""
        
"""


def test_coroutine():
    req = async_request("www.baidu.com")

    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(req)
    # task = loop.create_task(req)
    task.add_done_callback(callback_func)
    loop.run_until_complete(task)
    # 将回调函数绑定到任务对象中


def callback_func(task):
    print(task.result())


if __name__ == "__main__":
    # test_thread_pool()
    test_coroutine()
