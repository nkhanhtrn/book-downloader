import concurrent.futures
import img2pdf
import requests
import tempfile
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

def download_images(folder_name, urls):
    img_name = 1
    with tempfile.TemporaryDirectory() as tmpDirName:
        print(tmpDirName)
        for url in urls:
            ext = url.split('.')[-1]
            fp, path = tempfile.mkstemp('.' + ext, str(img_name) + '__', tmpDirName)
            with open(path, mode='wb') as f:
                img_name += 1
                response = requests.get(url)
                f.write(response.content)

        import glob
        with open(folder_name + ".pdf","wb") as f:
	        f.write(img2pdf.convert(glob.glob(tmpDirName + "/*." + ext)))
    

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

    for name in chapters:
        download_images(name, chapters[name])
        break

    duration = time.time() - start_time
    print(f"Downloaded in {duration} seconds")
