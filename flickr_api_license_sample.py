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


with open('apikey.txt', 'r') as f:
    API_KEY = f.read()[:-1]

flic = FlickrLicense(API_KEY)

# data directory setting
trgdirs = [
            'data/shrine_cln',
            # 'data/',
            ]

# fetch target filename
trgfiles = \
    [os.path.basename(path)
        for trgdir in trgdirs
            for path in glob.glob(os.path.join(trgdir, '*.jpg'))]

# extract photo id from file
trg_photo_ids = [filename.split('_')[0] for filename in trgfiles]

# photo_id:5798996673
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
# result
# result_str

import pickle
with open('shrine_cln_result.pkl', 'wb') as f:
    pickle.dump(result, f)

# output license file
license_file = 'shrine_cln_license.tsv'
with open(license_file, 'a', encoding='utf-8') as f:
    for line in result_str:
        f.write(line)
