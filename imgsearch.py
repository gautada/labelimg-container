#!/usr/bin/python3
from googleapiclient.discovery import build
import argparse
import hashlib
import requests
import shutil
import os
import PIL
from PIL import Image

def download(query="pennies", dest="pennies", key="", cx=""):
    if query is None or dest is None or key is None or cx is None:
        raise ValueError("None of the parameters can be None: query=%s dest=%s key=%s cx=%s" % (query, dest, key, cx))
    
    # Make sure destination exists
    if not os.path.isdir(dest):
        os.mkdir(dest)
    
    resource = build("customsearch", 'v1', developerKey=key).cse()
    start = 0
    while start <= 190:
        result = resource.list(q=query, cx=cx, searchType='image', start=start).execute()

        for item in result['items']:
            link = item['link']
            format = item['fileFormat']
            metadata = item['image']
            hash = hashlib.sha256(link.encode()).hexdigest()
            # print(item['fileFormat'])
            print(link)
            # print(hash)

            name = "%s.jpg" % hash
            if not os.path.isfile("%s/%s" % (dest, name)):
                tmp_file_name = "temp.img"
                try:
                    res = requests.get(link, stream=True, timeout=10)
                    if res.status_code == 200:
                        with open(tmp_file_name,'wb') as f:
                            shutil.copyfileobj(res.raw, f)
                        if "image/jpeg" != format:
                            im = Image.open(tmp_file_name)
                            rgb_im = im.convert('RGB')
                            rgb_im.save("%s/%s.jpg" % (dest, hash))
                        else:
                            os.rename(tmp_file_name, "%s/%s.jpg" % (dest, hash))
                        print("Success: %s" % hash)
                    else:
                        print("Error: Invalid response (%s)" % res.status_code)
                except requests.exceptions.ReadTimeout as rt:
                    print("Error: Fetch timed out")
                except requests.exceptions.SSLError as ssle:
                    print("Error: SSL")
                except requests.exceptions.ConnectionError as ce:
                    print("Error: Connection")
                except PIL.UnidentifiedImageError as piluie:
                    print("Error: Image format")
                    os.remove("temp.img")
            else:
                print("Skip: Image already exists")
        print()
    start = result['queries']['nextPage'][0]['startIndex']
    
        
if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='Image search and automated downloader.')
    parser.add_argument('--query', help='Image query parameter')
    parser.add_argument('--dest', default=None, help='Folder to save the downloaded images to (usually relative path)')
    parser.add_argument('--key', default=None, help='Google API key')
    parser.add_argument('--cx', default=None, help='Google Custom Search Engine ID')
    args = parser.parse_args()
    
    dest = None
    if 'IMG_SEARCH_DEST' in os.environ.keys():
        dest = os.environ['IMG_SEARCH_DEST']
    if args.dest is not None:
        dest = args.dest
    
    key = None
    if 'GOOGLE_KEY' in os.environ.keys():
        key = os.environ['GOOGLE_KEY']
    if args.key is not None:
        key = args.key
    
    cx = None
    if 'GOOGLE_CX' in os.environ.keys():
        cx = os.environ['GOOGLE_CX']
    if args.cx is not None:
        cx = args.cx
        
    download(query=args.query, dest=dest, key=key, cx=cx)


