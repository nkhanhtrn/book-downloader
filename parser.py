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
    start_time = time.time()

    def download_img(url):
        global my_lock
        global img_count
        img_name = ''
        with my_lock:
            img_name = str(img_count).zfill(4)
            img_count += 1
        fp, path = tempfile.mkstemp('.jpg', img_name + '__', tmpDirName)

        with open(path, mode='wb') as f:
            response = requests.get(url)
            f.write(response.content)
        
        return img_name

    with tempfile.TemporaryDirectory() as tmpDirName:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(download_img, urls) 
        
        import glob
        with open(folder_name + ".pdf","wb") as f:
            f.write(img2pdf.convert(sorted(glob.glob(tmpDirName + "/*.jpg"))))

        duration = time.time() - start_time
        print(f"Finished download {folder_name} in {duration}s.")


if __name__ == "__main__":
    domain = 'https://kissmanga.org'
    manga_url = '/manga/gd924067'
    start_time = time.time()
    img_count = 1
    my_lock = threading.Lock()

    chapter_urls = []
    chapter_urls = get_chapters_url(domain, manga_url)
    chapters = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for (name, urls) in executor.map(get_images_url, chapter_urls):
            chapters[name] = urls

    for name in chapters:
        download_images(name, chapters[name])

    duration = time.time() - start_time
    print(f"Finished in {duration} seconds")
