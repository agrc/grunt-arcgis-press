#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Server(object):
    _baseurl_format = 'http{0}://{1}{2}/{3}/'
    _token_url = '{0}tokens/generateToken'
    _create_service_url = '{0}admin/services/createService'
    _exists_url = '{0}admin/services/exists'
    _delete_service_url = '{0}admin/services/{1}/{2}.{3}/delete'

    def __init__(self,
                 username,
                 password,
                 host='localhost',
                 instance_name='arcgis',
                 use_https=False,
                 use_port=False,
                 port='6080'):

        self._use_https = use_https
        self._use_port = use_port
        self._instance = instance_name
        self._server = host
        self._port = port
        self.username = username
        self.password = password

        self._baseurl = self._format_base_url()

    def get_token_url(self):
        return self._token_url.format(self._baseurl)

    def get_create_service_url(self):
        return self._create_service_url.format(self._baseurl)

    def get_exists_url(self):
        return self._exists_url.format(self._baseurl)

    def get_delete_service_url(self, folder, service, type):
        return self._delete_service_url.format(
            self._baseurl, folder, service, type)

    def _format_base_url(self):
        https = ''
        if self._use_https:
            https = 's'

        port = ''
        if self._use_port:
            port = ':{0}'.format(self._port)

        return self._baseurl_format.format(https,
                                           self._server,
                                           port,
                                           self._instance)
