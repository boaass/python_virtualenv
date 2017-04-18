# -*- coding: utf-8 -*-

import requests
import os
import time
import random
import threading
from bs4 import BeautifulSoup


class WorkerThread(threading.Thread):
    def __init__(self, func, thread_id, img_url, img_name):
        super(WorkerThread, self).__init__()
        self.thread_id = thread_id
        self.func = func
        self.img_url = img_url
        self.img_name = img_name

    def run(self):
        print ('线程%d启动' % self.thread_id)
        self.func(self.img_url, self.img_name)
        print ('线程%d结束' % self.thread_id)


def request_html():
    fp = open(os.path.expanduser('~') + '/Desktop/top250.txt', mode='a+')
    index = 0
    for ID in range(0, 10):
        url = 'https://movie.douban.com/top250?start=' + str(ID * 25)
        res = requests.get(url=url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')

        for item in soup.select('li'):
            # 解析片名
            first_name = ''
            title_info = item.select('.info')
            if len(title_info) > 0:
                index = index + 1
                movie_content = title_info[0]
                hd = movie_content.select('.hd')
                if len(hd) > 0:
                    a = hd[0].select('a')
                    if len(a) > 0:
                        movie_names = a[0].select('span')
                        if len(movie_names) > 0:
                            fp.write(str(index) + '.\n' + '片名:')
                            first_name = movie_names[0].text.encode('utf-8').replace(' / ', '/')
                            for movie_name in movie_names:
                                name = movie_name.text.encode('utf-8').replace(' / ', '/')
                                fp.write(name)
                                print name
                            fp.write('\n')
            # 解析大图
            img = item.select('img')
            if len(img):
                img_url = img[0].get('src').encode('utf-8')
                setup_thread(index, img_url, first_name)
                fp.write('图片:' + img_url + '\n')
                print img_url

        time.sleep(random.randint(3, 5))
    fp.close()


def setup_thread(thread_id, img_url, img_name):
    thread = WorkerThread(download_img, thread_id, img_url, img_name)
    thread.start()
    thread.join()


def download_img(url, img_name):
    img_dir = os.path.expanduser('~') + '/Desktop/top250_img'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    img_name = img_name + os.path.splitext(url)[-1]
    img_path = img_dir + '/' + img_name

    img_request = requests.get(url)
    if img_request.status_code == 200:
        with open(img_path, 'wb') as f:
            for chunk in img_request.iter_content(chunk_size=1024):
                f.write(chunk)
                f.flush()
            f.close()


if __name__ == '__main__':
    request_html()
