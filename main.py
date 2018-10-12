import requests
import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = ''
HOMEPAGE = ''
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
RESOURCE_DIRECTORY = PROJECT_NAME + '/resources'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        do_task(url)
        queue.task_done()



def do_task(url):
    content_type = ''
    try:
        resp = requests.head(url)
        # checking if the link is a webpage or a file
        content_type = resp.headers['Content-Type']

        if 'text/html' in content_type:
            Spider.crawl_page(threading.current_thread().name, url)
        else: 
            # the link contains a file
            Spider.crawl_file(threading.current_thread().name, url, content_type)
            
    except Exception as e:
        pass
    


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
