""""
=============================
Flickr API sample
=============================

trial of following page
http://qiita.com/ichiroex/items/605fec47b3188b31bd53

ImageNet
http://cs.stanford.edu/people/karpathy/ilsvrc/

Todo:
-------------
- add license info getter


ODA, Daisuke
2017.3.12
"""

from __future__ import print_function, unicode_literals
import os
import sys
import logging
import time
from flickrapihelper import FlickrSearch, FlickrImageDownloader


# Get logger
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename='flickr_api.log')
logger = logging.getLogger()

# Flickr API KEY
# http://techbooster.org/android/mashup/14828/
with open('apikey.txt', 'r') as f:
    API_KEY = f.read()[:-1]

license = '4,5,6,9,10' # commercial use allowed

search_text_list = ['glasses']
search_text_list = ['fried noodle']
search_text_list = ['church', 'temple']
search_text_list = ['ramen', 'spaghetti']
search_text_list = ['dog', 'cat', 'bird', 'car', 'bicycle']
search_text_list = ['bicycle']
search_text_list = ['shrine', u'神社', 'temple', u'寺']
search_text_list = ['temple', u'寺']

#------------------------------------------------------
# Download images
#------------------------------------------------------

fckr = FlickrImageDownloader(API_KEY, license=license, logger=logger)

for search_text in search_text_list:

    dl_dir = os.path.join('data', search_text, 'src')
    if not os.path.exists(dl_dir):
        os.makedirs(dl_dir)

    fckr.search_download(search_text, dl_dir, n_photo=1000,
        verbose=True)

    time.sleep(60)
