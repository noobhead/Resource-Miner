import requests
from datatype import DataType
from link_finder import LinkFinder
from domain import *
from general import *


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    resources_dir = ''
    queue = set()
    crawled = set()

    ### Initialisations for Resources fpr Supported formats
    img = DataType('image')
    vid = DataType('video')
    aud = DataType('audio')
    pdf = DataType('pdf')
    csv = DataType('csv')
    oth = DataType('other')
    doc = DataType('doc')
    xls = DataType('excel')
    ppt = DataType('ppt')

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.resources_dir = Spider.project_name + '/resources'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        make_dir(Spider.resources_dir)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)


    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = requests.get(page_url)
            if 'text/html' in response.headers['Content-Type']:
                html_string = response.text
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)


    # download a file from url
    @staticmethod
    def download_file(url, file):
        resp = requests.get(url)
        f = open(file, 'wb')
        f.write(resp.content)
        f.close()


    # parses th type of document
    @staticmethod
    def crawl_file(thread_name, url, content_type):
        if url not in Spider.crawled:
            file_type = ''
            ###### for IMAGES######
            if 'image' in content_type:
                file_type = 'image'
                #make directory for resource if it doesn't exists already
                directory = Spider.resources_dir + '/images'
                make_dir(directory)
                file = directory + "/" + Spider.img.counter_name() + "." + content_type.split('/')[-1]


            ###### for VIDEOS######
            elif 'video' in content_type:
                file_type = 'video'
                #make directory for resource if it doesn't exists already
                directory = Spider.resources_dir + '/videos'
                make_dir(directory)
                file = directory + "/" + Spider.vid.counter_name() + "." + content_type.split('/')[-1]


            ###### for AUDIOS######
            elif 'audio' in content_type:
                file_type = 'audio file'
                #make directory for resource if it doesn't exists already
                directory = Spider.resources_dir + '/audios'
                make_dir(directory)
                file = directory + "/" + Spider.aud.counter_name() + "." + content_type.split('/')[-1]

                
            ###### for PDFs######
            elif 'application/pdf' in content_type:
                file_type = 'pdf file'
                #make directory for resource if it doesn't exists already
                directory = Spider.resources_dir + '/pdfs'
                make_dir(directory)
                file = directory + "/" + Spider.pdf.counter_name() + ".pdf"

            ###### for CSVs######
            elif 'text/csv' in content_type:
                file_type = 'csv file'
                #make directory for resource if it doesn't exists already
                directory = Spider.resources_dir + '/CSVs'
                make_dir(directory)
                file = directory + "/" + Spider.csv.counter_name() + "." + content_type.split('/')[-1]

            ###### for WORD FILES(doc or docx file)######
            elif "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in content_type:
                file_type = 'word file'
                #make directory for resource if it doesn't exists already
                directory = Spider.resources_dir + '/Word_files'
                make_dir(directory)
                file = directory + "/" + Spider.doc.counter_name() + ".docx"

            ###### for EXCEL FILES(xls or xlsx file)######
            elif "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or "application/vnd.ms-excel" in content_type:
                file_type = 'excel file'
                #make directory for resource if it doesn't exists already
                directory = Spider.resources_dir + '/Excel_files'
                make_dir(directory)
                file = directory + "/" + Spider.xls.counter_name() + ".xlsx"

            ###### for PPT FILES(ppt or pptx file)######
            elif "application/vnd.openxmlformats-officedocument.presentationml.presentation" or "application/vnd.ms-powerpoint" in content_type:
                file_type = 'ppt file'
                #make directory for resource if it doesn't exists already
                directory = Spider.resources_dir + '/PPT_files'
                make_dir(directory)
                file = directory + "/" + Spider.ppt.counter_name() + ".pptx"

            print(thread_name + " now downloading " + file_type)
            Spider.download_file(url, file)
            Spider.queue.remove(url)
            Spider.crawled.add(url)
            Spider.update_files()
