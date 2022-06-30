import os 
import sys
from unicodedata import name
import requests

from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread

class DownloadBiaoQingBao(Thread):
    def __init__(self,queue,path):
        Thread.__init__(self)
        self.queue = queue
        self.path = '/Users/camus/wistbean/biaoqingbao/'
        if not os.path.exists(path):
            os.makedirs(path)
    def run(self):
        while True:
            url = self.queue.get()
            try:
                # print(url)
                download_biaoqingbaos(self.path,url)
            finally:
                self.queue.task_done()
            
def download_biaoqingbaos(path,url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'lxml')
    imglist = soup.find_all('img', class_='ui image lazy')
    
    for img in imglist:
        image = img.get('data-original')
        title = img.get('title')
        
        try:
            with open(path + title + os.path.splitext(image)[-1],'wb') as f:
                img = requests.get(image).content
                f.write(img)
        except OSError:
            print('length  failed')
            break
    
if __name__ == '__main__':
    _url = 'https://fabiaoqing.com/biaoqing/lists/page/{page}.html'
    urls = [_url.format(page=page) for page in range(1, 4328+1)]
    queue = Queue()
    path = '/Users/camus/wistbean/biaoqingbao/'

    # 创建线程
    for x in range(10):
        worker = DownloadBiaoQingBao(queue, path)
        worker.daemon = True
        worker.start()

    # 加入队列
    for url in urls:
        queue.put(url)

    queue.join()
