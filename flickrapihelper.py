""""
=============================
Flickr API Hepler

You can
- search photos
- download photos
=============================

http://qiita.com/ichiroex/items/605fec47b3188b31bd53

Todo
-----
- Get license info for each image

ODA, Daisuke
2017.3.12
"""

from __future__ import print_function, unicode_literals

import os
import math
import json
import glob
import time

import urllib
import urllib2
import hashlib

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers




#------------------------------------------------------------------

class FlickrSearch(object):

    api_method = 'flickr.photos.search'
    url_root = 'https://api.flickr.com/services/rest/'

    max_n_photo = 500

    __search_format = 'json'
    __search_nojsoncallback = '1'

    def __init__(
                self,
                api_key,
                n_photo=10,
                sort='relevance',
                privacy_filter=1,
                license='10', # public domain
                content_type=1, # 1 for photos only
                ):

        """

        Paramater
        ------------------------
        license: str
            You can specify multiple value with comma-separated format
            e.g. '1,4,5'

        """

        # calc how many pages required to fetch all photos
        self.page_list, self.per_page_list = self._page_info(n_photo)

        self.search_param = {}

        # required params
        self.search_param['method'] = FlickrSearch.api_method
        self.search_param['api_key'] = api_key

        # optional params
        self.search_param['sort'] = sort
        self.search_param['privacy_filter'] = privacy_filter
        self.search_param['license'] = license
        self.search_param['content_type'] = content_type

        # fixed params
        self.search_param['format'] = FlickrSearch.__search_format
        self.search_param['content_type'] = \
            FlickrSearch.__search_nojsoncallback

        self.response_dict = None


    @staticmethod
    def _page_info(n_photo):
        n_pages = int(math.ceil(float(n_photo) / FlickrSearch.max_n_photo))
        rest_img = n_photo % FlickrSearch.max_n_photo

        page_list = list(range(1, n_pages + 1))
        if rest_img == 0:
            per_page_list = [FlickrSearch.max_n_photo] * n_pages
        else:
            per_page_list = [FlickrSearch.max_n_photo] * (n_pages - 1) + [rest_img]

        return page_list, per_page_list


    def _get_response(self, url, search_text):
        """Return response from search API as json string

        Params
        -------------
        url: str
            API uri include optional query string
        search_text: str (multibyte words should be URLencoded)
            search word

        Returns
        -------------
        str, json as response from API
        """
        register_openers()
        datagen, headers = multipart_encode({'text': search_text})
        request = urllib2.Request(url, datagen, headers)
        response = urllib2.urlopen(request)
        return response.read()


    @staticmethod
    def _bulid_photo_uri(farm, server, id, secret, **keyword):
        """Bulid photo uri

        ## Photo URL
        https://www.flickr.com/services/api/misc.urls.html
        """
        url_template = \
            'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg'
        return url_template.format(
                                    farm=farm,
                                    server=server,
                                    id=id,
                                    secret=secret
                                    )


    @staticmethod
    def _get_photo_urilist(response_dict):
        return [ FlickrSearch._bulid_photo_uri(**phto_info)
            for phto_info in response_dict['photos']['photo'] ]


    def save_response(self, file_name):
        if self.response_string is not None:
            with open(file_name, 'w') as f:
                f.write(self.response_string)


    @staticmethod
    def _get_dict(response_string):
        prefix_api = 'jsonFlickrApi('
        if response_string[:len(prefix_api)] == prefix_api:
            json_string = response_string[len(prefix_api):-1]
            return json.loads(json_string)
        elif response_string[0] == '{':
            return json.loads(response_string)
        else:
            raise Exception('Invalid response string format')


    @staticmethod
    def _check_reponse(response_dict):
        error_keys = ['stat', 'code', 'message']
        if len([ k for k in response_dict.keys() if k in error_keys]) \
            == len(error_keys):
            raise Exception(str(response_dict))


    def search(self, search_text, n_photo=10, **keywords):
        """Search flickr web for image relevant to search_text

            Returns: list of url string
        """

        # how many pages required to fetch all photos
        self.page_list, self.per_page_list = self._page_info(n_photo)

        # update default search param
        for key, value in keywords.items():
            if key in self.search_param.keys():
                self.search_param.update({key: value})

        # Bulid query string from dict and urlencode value
        # simultaneously
        api_urls = []
        for page, per_page in zip(self.page_list, self.per_page_list):
            search_param = self.search_param.copy()
            search_param.update({'page': page, 'per_page': per_page})
            query_string = urllib.urlencode(search_param)
            api_url = '{root}?{param}'.format(root=self.url_root,
                param=query_string)
            api_urls.append(api_url)

        self.search_api_urls = api_urls

        # search
        photo_urls = []
        for api_url in api_urls:
            response_string = self._get_response(api_url, search_text)
            response_dict = self._get_dict(response_string)
            self._check_reponse(response_dict)
            self.response_string = response_string
            self.response_dict = response_dict
            photo_urls.extend(self._get_photo_urilist(response_dict))

        return photo_urls


#------------------------------------------------------------------

class URIDownloader(object):

    hash_func = hashlib.md5

    @staticmethod
    def _get_hash(file_list):
        hash_list = {}
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                hash_list[file_name] = \
                URIDownloader.hash_func(f.read()).hexdigest()
        return hash_list


    def download(self, uri_list, out_dir, wait_sec=2, logger=None,
                verbose=False):

        pattern = '*.jpg'

        # check existing files in out_dir
        existing_files = glob.glob(os.path.join(out_dir, pattern))
        existing_files_hash = \
            FlickrImageDownloader._get_hash(existing_files)

        # iter all files in list and download them all
        for idx, url in enumerate(uri_list):

            outfile = os.path.basename(url)
            outpath = os.path.join(out_dir, outfile)

            # check if same file name exists
            # if exists then skip download
            if not os.path.exists(outpath):

                flickr_file = urllib2.urlopen(url)
                flickr_file_data = flickr_file.read()
                flickr_file_hash = URIDownloader.hash_func(flickr_file_data)

                # check if same hash exists
                # if exists then skip download
                if flickr_file_hash not in existing_files_hash.values():
                    with open(outpath, 'wb') as f:
                        f.write(flickr_file_data)
                    time.sleep(wait_sec)
                    msg_proc = 'Downloaded'

                else:
                    conflict_file = \
                        [ f for f, h in existing_files_hash.items() \
                        if h == flickr_file_hash ][0]
                    msg_proc = """Skipped.\n Same hash exists. \n
                            flickr_file:{0}existing_file:{1}""".format(
                                flickr_file, conflict_file)

            else:
                msg_proc = 'Skipped. Same file name exists'

            msg = 'idx:{idx}\tfile:{file}\tstatus:{status}'.format(
                idx=idx,
                file=outfile,
                status=msg_proc)
            self._logging(msg, 'info', logger=logger, verbose=verbose)

    @staticmethod
    def _logging(msg, method, logger, verbose):
        if logger is not None:
            getattr(logger, method)(msg)
        if verbose:
            print(msg)


#------------------------------------------------------------------

class FlickrImageDownloader(FlickrSearch, URIDownloader):

    def __init__(self,
                api_key,
                n_photo=10,
                sort='relevance',
                privacy_filter=1,
                license='10',
                content_type=1, # photos only
                logger=None):

        super(FlickrImageDownloader, self).__init__(
                api_key=api_key,
                n_photo=n_photo,
                sort=sort,
                privacy_filter=privacy_filter,
                license=license,
                content_type=content_type # photos only
                )

        self.logger = logger

    def search_download(self, search_text, out_dir,
                        n_photo=10, wait_sec=2, verbose=False, **keywords):
        uri_list = self.search(search_text, n_photo, **keywords)
        self.download(uri_list, out_dir, wait_sec,
            logger=self.logger, verbose=verbose)
