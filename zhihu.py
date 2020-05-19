import threading
from lxml import etree
import requests
import queue

# 获取url队列
def preparUrlQueue():
    urlqueue = queue.Queue()
    url = 'https://www.zhihu.com/hot'
    headers = {
        'Cookie': 'q_c1=....',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    response = etree.HTML(r.text)
    detail_url = response.xpath(
        '//div[@class="HotList-list"]/section[@class="HotItem"]/div[@class="HotItem-content"]/a/@href')

    for i in detail_url:
        urlqueue.put(i)
    return urlqueue
# 采集线程组
class CrawlerThread(threading.Thread):
    def __init__(self,name,urlqueue):
        super().__init__(name=name)
        self.urlqueue=urlqueue
    def run(self):
        print(f'{self.name}采集线程正在执行')
        # 循环提取数据，不空就执行
        while not self.urlqueue.empty():
            try:
                headers = {
                    'Cookie': 'q_c1=...',
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                }
                url=self.urlqueue.get(block=False)
                detail_response=requests.get(url,headers=headers)
                detail_text = detail_response.text
                # 把响应放到响应队列中
                responsequeue.put(detail_text)


            except:
                pass
# 解析线程组
class PaserThread(threading.Thread):
    def __init__(self,name,responsequeue):
        super().__init__(name=name)
        # 拿到响应队列
        self.responsequeue=responsequeue
    def run(self):
        print(f'{self.name}采集线程正在执行')
        # 循环提取数据，不空就执行
        while is_full:
            try:
                # 获取response
                response=self.responsequeue.get(block=False)
                self.parseResponse(response)

            except:
                pass
    def parseResponse(self,response):
        detail_html = etree.HTML(response)
        detail_content = detail_html.xpath(
            '//div[@class="QuestionHeader-detail"]/div/div/span[@class="RichText ztext"]//text()')

        if len(detail_content) > 0:
            detail_content = detail_content[0]
        else:
            detail_content = '空'

        nickname = detail_html.xpath(
            '//div[@class="ContentItem AnswerItem"]/div[@class="ContentItem-meta"]/div[@itemprop="author"]/meta[@itemprop="name"]/@content')

        # print(nickname)
        voters = detail_html.xpath('//div[@class="css-h5al4j"]/span/span[@class="Voters"]/button/text()')
        # print(voters)

        wirtertime = detail_html.xpath(
            '//div[@class="RichContent RichContent--unescapable"]/div[2]/div[@class="ContentItem-time"]/a/span/@data-tooltip')

        # print(wirtertime)
        good = detail_html.xpath('//button[@class="Button VoteButton VoteButton--up"]/@aria-label')
        # print(good)
        speaknum = detail_html.xpath(
            '//button[@class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"][1]/text()')
        # print(speaknum)


if __name__ == '__main__':
    print('主线程开始')
    lock=threading.Lock()
    urlqueue=preparUrlQueue()
    responsequeue=queue.Queue()
    is_full = True
    crawlerThread=[]
    for i in range(50):
        thread=CrawlerThread(f'{i}号线程正在执行',urlqueue)
        crawlerThread.append(thread)
    for t in crawlerThread:
        t.start()

    # 启动解析线程
    paserThread=[]
    for i in range(10):
        thread=PaserThread(f'{i}号线程正在执行',responsequeue)
        paserThread.append(thread)
    for i in paserThread:
        i.start()
    # 判断urlqueue是否为空
    while not urlqueue.empty():
        pass
    # 采集线程组的join
    for t in crawlerThread:
        t.join()
    # responsequeue
    while not responsequeue.empty():
        pass
    is_full=False
#     解析线程组的jion
    for t in paserThread:
        t.join()
    print('主线程退出')





