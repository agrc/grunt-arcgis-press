#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
press
----------------------------------
the main module
'''

from services import GetTokenCommand, ServiceExistsCommand, GetServiceJsonCommand, EditServiceCommand
from models import Server
from os import getcwd
from os.path import join
from wrapper import Py


class Press(object):

    def __init__(self, serverProperties, tempFolder):
        super(Press, self).__init__()

        self._server = Server(**serverProperties)
        self._tempFolder = tempFolder or join(getcwd(), '.temp')
        self.py = Py()

        command = GetTokenCommand(self._server)
        self._token = command.execute()

    def stage(self, serviceConfig):
        connection_file = self.py.get_server_connection_file(self._server, self._tempFolder)
        # print('connection file created')

        sddraft = self.py.create_sd_draft(self._tempFolder, connection_file, **serviceConfig)
        # print('drafted')

        data = {
            'token': self._token,
            'name': serviceConfig['serviceName'],
            'type': serviceConfig['type'],
            'folder': ''
        }

        if 'folder' in serviceConfig:
            data['folder'] = serviceConfig['folder']

        command = ServiceExistsCommand(self._server.get_exists_url(), data)

        exists = command.execute()

        if(exists):
            self.py.modify_sd_for_replacement(sddraft)

        sd = self.py.stage_service(sddraft)
        # print('staged')

        print(sd.getOutput(0))
        print(connection_file)
        return 0

    def upload(self, sd, connection_file):
        self.py.upload_service(sd, connection_file)

        print('uploaded')

    def edit(self, serviceConfig):
        data = {
            'token': self._token,
            'name': serviceConfig['serviceName'],
            'type': serviceConfig['type'],
            'folder': ''
        }

        if 'folder' in serviceConfig:
            data['folder'] = serviceConfig['folder']

        url = self._server.get_service_info_url(data['name'],
                                                data['type'],
                                                data['folder'])
        command = GetServiceJsonCommand(url, data)
        json = command.execute()

        url = self._server.get_edit_service_url(data['name'],
                                                data['type'],
                                                data['folder'])

        command = EditServiceCommand(self._token,
                                     url,
                                     json,
                                     serviceConfig)

        command.execute()

        print('{} published successfully to {}'.format(
            serviceConfig['serviceName'],
            self._server._host))

    def __repr__(self):
        return '''
        Press
            temp folder: {}
            server: {}'''.format(self._tempFolder, self._server)
