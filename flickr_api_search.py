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
- add license info


ODA, Daisuke
2017.3.12
"""

from __future__ import print_function, unicode_literals
import sys
import os
import logging
import time

from flickrapihelper import FlickrSearch, FlickrImageDownloader
from utils import PathBuilder, ImageValidationSplitter


# Get logger
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename='flickr_api.log')


logger = logging.getLogger()
#logger.addHandler(logging.StreamHandler())

# Flickr API KEY
# http://techbooster.org/android/mashup/14828/
API_KEY = 'd312e6793d7fec1136e4950ba249591d'

license = '4,5,6,9,10' # commercial use allowed


search_text_list = ['glasses']
search_text_list = ['fried noodle']

#------------------------------------------------------
# Get images URL only
#------------------------------------------------------

fs = FlickrSearch(API_KEY)
jpg_list = fs.search(search_text='dog', n_photo=1000)
len(jpg_list)
fs.per_page_list
fs.page_list
#------------------------------------------------------
# Download images
#------------------------------------------------------

fckr = FlickrImageDownloader(API_KEY, license=license, logger=logger)

for search_text in search_text_list:

    pathb = PathBuilder(search_text)
    out_dir = pathb.get_outdir('src')
    pathb.mkdir(out_dir)

    fckr.search_download(search_text, out_dir, n_photo=200,
        verbose=True)

    time.sleep(60)


#------------------------------------------------------
# Split images into test and train
#------------------------------------------------------

for search_text in search_text_list:

    pathb = PathBuilder(search_text, root_dir='data_rs_3class')
    splt = ImageValidationSplitter(pathb)

    print(search_text, splt.get_file_count('src'))

    splt.split(ratio={'train': 0.7, 'validation': 0.2, 'test': 0.1}, copy=True, add_classlabel=True)
