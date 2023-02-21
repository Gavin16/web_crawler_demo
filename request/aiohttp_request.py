
import aiohttp
import time
import asyncio


async def http_request(url):
    print("请求地址:", url)
    async with aiohttp.ClientSession() as session:
        async with await session.get(url) as response:
            # 这里获取响应数据操作之前要使用await进行手动挂起
            page_text = await response.text()
            # page_bin = await response.read()
            # req_json = await response.json()
            print(page_text)


def aio_request_test():
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
    start = time.time()
    aio_request_test()
    end = time.time()
    print("执行总耗时:", end - start)