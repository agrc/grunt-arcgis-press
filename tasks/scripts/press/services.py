#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from models import Server


def _make_request(url, data):
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


class GetTokenCommand(object):

    def __init__(self, serverProperties):
        self._server = Server(**serverProperties)

    def execute(self):
        token_url = self._server.get_token_url()

        payload = {
            'username': self._server.username,
            'password': self._server.password,
            'f': 'json'
        }

        response = _make_request(token_url, payload)

        return response['token']


class PublishCommand(object):
    def __init__(self, token, service_json, serverProperties):
        super(PublishCommand, self).__init__()

        # TODO: create defaults for other service types
        defaults = json.loads(open('./configs/mapservice.json').read())

        self._token = token
        self._service = self._deep_merg(defaults, service_json)
        # self._service = defaults
        self._server = Server(**serverProperties)

    def _deep_merg(self, d1, d2):
        for item in d2:
            if item in d1 and type(d2[item]) is dict:
                for leaf in d2[item]:
                    d1[item][leaf] = d2[item][leaf]
            else:
                d1[item] = d2[item]
        return d1

    def _exists(self):
        exists_url = self._server.get_exists_url()
        payload = {
            'token': self._token,
            # TODO: implement folder names in service configs
            'folderName': '',
            'serviceName': self._service['serviceName'],
            'serviceType': self._service['type'],
            'f': 'json'
        }

        return _make_request(exists_url, payload)

    def _delete_service(self):
        delete_url = self._server.get_delete_service_url(
            '', self._service['serviceName'], self._service['type'])
        payload = {
            'token': self._token,
            'f': 'json'
        }

        _make_request(delete_url, payload)

    def execute(self):
        if self._exists():
            self._delete_service()

        creation_url = self._server.get_create_service_url()
        payload = {
            'token': self._token,
            'service': json.dumps(self._service),
            'f': 'json'
        }

        return _make_request(creation_url, payload)
