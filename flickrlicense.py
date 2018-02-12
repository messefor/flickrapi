
import json

import requests
import urllib.parse


class FlickrLicense(object):

    # API URL
    _url_root = 'https://api.flickr.com/services/rest/'

    # method
    _method_photo_getinfo = 'flickr.photos.getInfo'
    _method_license_getinfo = 'flickr.photos.licenses.getInfo'
    _method_people_getinfo = 'flickr.people.getInfo'

    # url params fixed
    __out_format = 'json'
    __out_nojsoncallback = '1'


    def __init__(self, api_key):

        self.api_key = api_key

        # fixed params
        self.url_param_cmn = {}

        self.url_param_cmn['format'] = FlickrLicense.__out_format
        self.url_param_cmn['content_type'] = \
            FlickrLicense.__out_nojsoncallback
        self.url_param_cmn['api_key'] = api_key

        #  list of available photo licenses for Flickr.
        self.license_list = None


    def _url_getlicense(self):

        url_param = self.url_param_cmn.copy()
        url_param.update({
                            'method': FlickrLicense._method_license_getinfo})
        query_string = urllib.parse.urlencode(url_param)
        api_url = '{root}?{param}'.format(root=self._url_root,
            param=query_string)

        return api_url


    def _ref_license(self, license_num):

        if self.license_list is None:
            self.license_list = self._getLicenseInfo()['licenses']['license']

        license_info = \
            [ elm for elm in self.license_list if str(elm['id']) == str(license_num) ][0]

        return license_info


    def _getLicenseInfo(self):
        """ Return PhotoInfo

        Return
        ---------
        dict {}

        """
        api_url = self._url_getlicense()
        res_json = self._get_response(api_url)
        return self._get_dict(res_json)


    def _url_getpeopleinfo(self, user_id):

        url_param = self.url_param_cmn.copy()
        url_param.update({'method': FlickrLicense._method_people_getinfo,
                            'user_id': user_id})
        query_string = urllib.parse.urlencode(url_param)
        api_url = '{root}?{param}'.format(root=self._url_root,
            param=query_string)

        return api_url


    def _getPeopleInfo(self, user_id):
        """ Return PeopleInfo

        Return
        ---------
        dict {}

        """
        api_url = self._url_getpeopleinfo(user_id)
        res_json = self._get_response(api_url)
        res_dict = self._get_dict(res_json)
        return self._select_person_info(res_dict)


    def _url_getphotoinfo(self, photo_id):

        url_param = self.url_param_cmn.copy()
        url_param.update({
                            'method': FlickrLicense._method_photo_getinfo,
                            'photo_id': photo_id})

        query_string = urllib.parse.urlencode(url_param)
        api_url = '{root}?{param}'.format(root=self._url_root,
            param=query_string)

        return api_url


    def _getPhotoInfo(self, photo_id):
        """ Return PhotoInfo

        Return
        ---------
        dict {}

        """
        api_url = self._url_getphotoinfo(photo_id)
        res_json = self._get_response(api_url)
        res_dict = self._get_dict(res_json)

        return self._select_photo_info(res_dict)


    @staticmethod
    def _get_response(url):
        """Return response from search API as json string

        Params
        -------------
        url: str
            API uri include optional query string

        Returns
        -------------
        str, json as response from API
        """
        response = requests.post(url)

        if response.status_code in (200,):
            return response.content.decode('utf-8')
        else:
            raise Exception

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
    def _get_elm_by_str(x, evalstr):
        try:
            result = eval(evalstr)
        except (KeyError, IndexError):
            result = None
        return result


    def _select_photo_info(self, response_dict):

        if response_dict['stat'] == 'ok':

            return_dict = {}

            photo = response_dict['photo']

            return_dict['photo_id'] = self._get_elm_by_str(photo, "x['id']")
            return_dict['license'] = self._get_elm_by_str(photo, "x['license']")

            first_author = self._get_elm_by_str(photo, "x['notes']['note'][0]")

            if first_author is not None:
                return_dict['author'] = self._get_elm_by_str(first_author, "x['author']")

                return_dict['authorname'] = self._get_elm_by_str(first_author, "x['authorname']")

            return_dict['nsid'] = self._get_elm_by_str(photo, "x['owner']['nsid']")

            return_dict['title'] = self._get_elm_by_str(photo, "x['title']['_content']")

            return_dict['url'] = self._get_elm_by_str(photo, "x['urls']['url'][0]['_content']")

            return return_dict

        else:
            print('response_dict:', response_dict['stat'])
            raise Exception


    def _select_person_info(self, response_dict):

        if response_dict['stat'] == 'ok':

            return_dict = {}
            person = response_dict['person']

            return_dict['ispro'] = self._get_elm_by_str(person, "x['ispro']")
            return_dict['nsid'] = self._get_elm_by_str(person, "x['nsid']")
            return_dict['profileurl'] = self._get_elm_by_str(person, "x['profileurl']['_content']")

            return_dict['username'] = self._get_elm_by_str(person, "x['username']['_content']")

            return return_dict

        else:
            raise Exception


    def _fetch_all(self, photo_id):

        photo_info = self._getPhotoInfo(photo_id)

        license_info = None
        if photo_info['license']:
            license_info = self._ref_license(license_num=photo_info['license'])

        user_id = photo_info['nsid']
        people_info = None
        if user_id:
            people_info = self._getPeopleInfo(user_id)

        return {'photo': photo_info, 'license': license_info,
                                    'people': people_info}

    @staticmethod
    def _filter_allinfo(info_dict_all):

        filtered_dict = {
        'title': info_dict_all['photo']['title'],
        'title_url': info_dict_all['photo']['url'],
        'author': info_dict_all['people']['username'],
        'author_url': info_dict_all['people']['profileurl'],
        'license': info_dict_all['license']['name'],
        'license_id': info_dict_all['photo']['license'],
        'license_url': info_dict_all['license']['url'],}

        return filtered_dict


    def fetchInfo(self, photo_id):

        all_info = self._fetch_all(photo_id)
        return self._filter_allinfo(all_info)

    def out_lisence_str(self, photo_id):
        format_func = self.string_format_simple
        filtered_info = self.fetchInfo(photo_id)
        return format_func(filtered_info)

    @staticmethod
    def string_format_simple1(filtered_info):
        return '"{title}" by {author}'.format(**filtered_info)

    @staticmethod
    def string_format_simple(filtered_info):
        return 'CC by {author}'.format(**filtered_info)
