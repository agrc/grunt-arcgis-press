#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Server(object):
    _baseurl_format = 'http{0}://{1}{2}/{3}/'
    _token_url = '{0}tokens/generateToken'
    _exists_url = '{0}admin/services/exists'
    _edit_service_url = '{0}admin/services/{1}{2}.{3}/edit'
    _delete_service_url = '{0}admin/services/{1}{2}.{3}/delete'
    _service_info_url = '{0}admin/services/{1}{2}.{3}?f=json'

    def __init__(self,
                 username,
                 password,
                 host='localhost',
                 instance_name='arcgis',
                 use_https=False,
                 use_port=True,
                 port='6080'):

        self._use_https = use_https
        self._use_port = use_port
        self._instance = instance_name
        self._host = host
        self._port = port
        self.username = username
        self.password = password

        self._baseurl = self._format_base_url()

    def get_token_url(self):
        return self._token_url.format(self._baseurl)

    def get_edit_service_url(self, service, type, folder=''):
        if folder:
            folder = folder + '/'

        return self._edit_service_url.format(self._baseurl, folder, service, type)

    def get_exists_url(self):
        return self._exists_url.format(self._baseurl)

    def get_delete_service_url(self, service, type, folder=''):
        if folder:
            folder = folder + '/'

        return self._delete_service_url.format(
            self._baseurl, folder, service, type)

    def get_service_info_url(self, service, type, folder=''):
        if folder:
            folder = folder + '/'

        return self._service_info_url.format(
            self._baseurl, folder, service, type)

    def get_admin_url(self):
        return self._baseurl + 'admin'

    def _format_base_url(self):
        https = ''
        if self._use_https:
            https = 's'

        port = ''
        if self._use_port:
            port = ':{0}'.format(self._port)

        return self._baseurl_format.format(https,
                                           self._host,
                                           port,
                                           self._instance)

    def __repr__(self):
        return '''
        Server Model
            username: {}
            password: {}
            host: {}
            instance: {}
            https: {}
            port: {}
            use port:{}'''.format(self.username,
                                  self.password,
                                  self._host,
                                  self._instance,
                                  self._use_https,
                                  self._port,
                                  self._use_port)
