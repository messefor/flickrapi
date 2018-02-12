#-----------------------------------
# make license list from file
# ODA, Daisuke
# 2017.6.4
#-----------------------------------

import os
import glob
import time
import re

from flickrlicense import FlickrLicense


API_KEY = 'd312e6793d7fec1136e4950ba249591d'
flic = FlickrLicense(API_KEY)

# data directory setting
suffix = 'rs'
trgdirs = [
            #'../data/data_{}/test/unknown'.format(suffix),

            '../data/data_{}/train/ramen'.format(suffix),
            '../data/data_{}/train/spaghetti'.format(suffix),

            #'../data/data_{}/validation/ramen'.format(suffix),
            #'../data/data_{}/validation/spaghetti'.format(suffix),
            ]

# fetch target filename
trgfiles = \
    [ os.path.basename(path)
        for trgdir in trgdirs
            for path in glob.glob(os.path.join(trgdir, '*.jpg')) ]

# extract photo id from file
trg_photo_ids = [ filename.split('_')[-2] for filename in trgfiles ]

# check
len(trgfiles)
len(trg_photo_ids)
trg_photo_ids[:10]


# fetch license info
result = {}
result_str = []

delim = '\t'
for idx, photo_id in enumerate(trg_photo_ids):

    # license info detail
    info_dict = flic.fetchInfo(photo_id)
    info_dict['filename'] = trgfiles[idx]
    result[photo_id] = info_dict

    # license string formatted
    # replace delimiter in line, work around error on np.genfromtxt()
    lic = flic.out_lisence_str(photo_id).replace(delim, ' ')
    license_str = '{filename}{delim}{license}\n'.format(
        filename=trgfiles[idx],
        delim=delim,
        license=lic
        )

    result_str.append(license_str)

    time.sleep(1)


# check
result
result_str

# output license file
license_file = '{}_license.tsv'.format(suffix)
with open(license_file, 'a', encoding='utf-8') as f:
    for line in result_str:
        f.write(line)
