import concurrent.futures
from concurrent.futures import thread
import requests
import threading
import time
from bs4 import BeautifulSoup


thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def get_chapters_url(domain, manga_url):
    session = get_session()
    chapter_urls = []

    with session.get(domain + manga_url) as response:
        soup = BeautifulSoup(response.text, 'lxml')       
        for chapter in soup.select('.listing a'):
            chapter_urls.append(domain + chapter.get('href'))

    return chapter_urls


def get_images_url(url):
    session = get_session()
    image_urls = []
    chapter_name = ''
    
    with session.get(url) as response:
        soup = BeautifulSoup(response.text, 'lxml')
        
        # get chapter name
        for chapter in soup.select('#selectEpisode option'):
            if chapter.get('selected') is not None:
                chapter_name = chapter.text.strip()
                break
        
        for image in soup.select('#centerDivVideo img'):
            image_urls.append(image.get('src'))

    return (chapter_name, image_urls)

if __name__ == "__main__":
    domain = 'https://kissmanga.org'
    manga_url = '/manga/gd924067'
    start_time = time.time()

    chapter_urls = []
    chapter_urls = get_chapters_url(domain, manga_url)
    chapters = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for (name, urls) in executor.map(get_images_url, chapter_urls):
            chapters[name] = urls

    print(chapters.keys())
    duration = time.time() - start_time
    print(f"Downloaded in {duration} seconds")
