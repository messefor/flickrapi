""""
=============================
Flickr API sample
=============================
Python2 only

ImageNet
http://cs.stanford.edu/people/karpathy/ilsvrc/

Flickr Search API
# https://www.flickr.com/services/api/flickr.photos.search.html

Ref
http://qiita.com/ichiroex/items/605fec47b3188b31bd53

ODA, Daisuke
2017.3.12
"""

from __future__ import print_function, unicode_literals
import os
import logging
import time

from flickrapihelper import FlickrSearch, FlickrImageDownloader


# Flickr API KEY
# http://techbooster.org/android/mashup/14828/
with open('apikey.txt', 'r') as f:
    API_KEY = f.read()[:-1]


#------------------------------------------------------
# Get images URI
#------------------------------------------------------

fs = FlickrSearch(API_KEY)
jpg_list = fs.search(search_text='cat', n_photo=10)

for uri in jpg_list:
    print(uri)


#------------------------------------------------------
# Download images
#------------------------------------------------------

fckr = FlickrImageDownloader(API_KEY)
fckr.search_download(search_text='cat', out_dir='data/samples',
    n_photo=10, verbose=True)


#------------------------------------------------------
# With optional parametars
#
# Params
# https://www.flickr.com/services/api/flickr.photos.search.html
#------------------------------------------------------

# Get logger
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename='flickr_api.log')
logger = logging.getLogger()

#　API Params config
license = '4,5,6,9,10' # commercial use allowed
privacy_filter = '1' # 1 public photos
content_type = '1' # 1 photos only.

# Downloader instance
fckr = FlickrImageDownloader(API_KEY, license=license, logger=logger)

# Search and download images
fckr.search_download(search_text='dog', out_dir='data/samples',
    n_photo=10, privacy_filter = '1', verbose=True)
