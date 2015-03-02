#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


class HttpRequestable(object):

    def __init__(self):
        super(HttpRequestable, self).__init__()

    def post(self, url, data):
        r = requests.post(url, data=data)

        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        response = r.json()

        try:
            if response['status'] == 'error':
                raise BaseException(response['messages'][0])
        except:
            pass

        return response

    def get(self, url, data):
        r = requests.get(url, params=data)

        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        response = r.json()

        try:
            if response['status'] == 'error':
                raise BaseException(response['messages'][0])
        except:
            pass

        return response


class GetTokenCommand(HttpRequestable):

    def __init__(self, server):
        super(GetTokenCommand, self).__init__()

        self._server = server

    def execute(self):
        token_url = self._server.get_token_url()

        payload = {
            'username': self._server.username,
            'password': self._server.password,
            'f': 'json'
        }

        response = self.post(token_url, payload)

        return response['token']


class EditServiceCommand(HttpRequestable):

    def __init__(self, token, url, defaults, service_json):
        super(EditServiceCommand, self).__init__()

        self._token = token
        self._service = self._deep_merge(defaults, service_json)
        self._url = url

    def _deep_merge(self, d1, d2):
        for item in d2:
            if item in d1 and type(d2[item]) is dict:
                for leaf in d2[item]:
                    d1[item][leaf] = d2[item][leaf]
            else:
                d1[item] = d2[item]
        return d1

    def execute(self):
        payload = {
            'token': self._token,
            'service': json.dumps(self._service),
            'f': 'json'
        }

        return self.post(self._url, payload)


class DeleteServiceCommand(HttpRequestable):

    def __init__(self, url, token):
        super(DeleteServiceCommand, self).__init__()

        self.url = url
        self.data = {
            'token': token,
            'f': 'json'
        }


class ServiceExistsCommand(HttpRequestable):
    def __init__(self, url, data):
        super(ServiceExistsCommand, self).__init__()

        self.url = url
        self.data = {
            'token': data['token'],
            'folderName': data['folder'],
            'serviceName': data['name'],
            'type': data['type'],
            'f': 'json'
        }

    def execute(self):
        response = self.post(self.url, self.data)
        return bool(response['exists'])


class GetServiceJsonCommand(HttpRequestable):
    def __init__(self, url, data):
        super(GetServiceJsonCommand, self).__init__()

        self.url = url
        self.data = {
            'token': data['token'],
            'folderName': data['folder'],
            'serviceName': data['name'],
            'serviceType': data['type'],
            'f': 'json'
        }

    def execute(self):
        return self.get(self.url, self.data)
