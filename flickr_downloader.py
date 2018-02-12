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

sys.path.append('..')
from utils import PathBuilder, ImageValidationSplitter


# Get logger
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename='flickr_api.log')
logger = logging.getLogger()

# Flickr API KEY
# http://techbooster.org/android/mashup/14828/
API_KEY = 'd312e6793d7fec1136e4950ba249591d'
license = '4,5,6,9,10' # commercial use allowed

search_text_list = ['glasses']
search_text_list = ['fried noodle']
search_text_list = ['church', 'temple']
search_text_list = ['ramen', 'spaghetti']

search_text_list = ['dog', 'cat', 'bird', 'car', 'bicycle']

search_text_list = ['bicycle']
#------------------------------------------------------
# Download images
#------------------------------------------------------

fckr = FlickrImageDownloader(API_KEY, license=license, logger=logger)


for search_text in search_text_list:

    pathb = PathBuilder(search_text, root_dir='../data')
    out_dir = pathb.get_outdir('_src')
    pathb.mkdir(out_dir)

    fckr.search_download(search_text, out_dir, n_photo=400,
        verbose=True)

    time.sleep(60)
