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


# extract photo id from file
trg_photo_ids = [ filename.split('_')[-2] for filename in trgfiles ]

trg_photo_ids = [
    "9025419644",
    "5798996673",
    "8591553706",
    "11875314",
    "5693093248",
    "16567032883",
    "4600937658",
    "4782553809",
    "5193779215",
    "115186679",
    "3271516011",
    "8300890670",
    ]

# check
len(trg_photo_ids)


# fetch license info
result = []

delim = '\t'
for idx, photo_id in enumerate(trg_photo_ids):

    # license info detail
    info_dict = flic.fetchInfo(photo_id)
    info_dict['photo_id'] = trg_photo_ids[idx]
    #result[photo_id] = info_dict

    # license string formatted
    # replace delimiter in line, work around error on np.genfromtxt()
    #lic = flic.out_lisence_str(photo_id).replace(delim, ' ')

#    license_str = '{filename}{delim}{license}\n'.format(
#        filename=trgfiles[idx],
#        delim=delim,
#        license=lic
#        )

    result.append(info_dict)

    time.sleep(1)


# check
result
result_str

# output license file
#license_file = '{}_license.tsv'.format(suffix)
#with open(license_file, 'a', encoding='utf-8') as f:
#    for line in result_str:
#        f.write(line)
