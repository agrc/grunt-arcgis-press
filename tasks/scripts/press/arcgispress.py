#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
press
----------------------------------
the main module
'''

from services import GetTokenCommand, PublishCommand


class Press(object):

    def __init__(self, serviceConfig, serverProperties):
        super(Press, self).__init__()

        self.serviceConfig = serviceConfig
        self.serverProperties = serverProperties

        self.execute()

    def execute(self):
        command = GetTokenCommand(self.serverProperties)
        token = command.execute()
        command = PublishCommand(token,
                                 self.serviceConfig,
                                 self.serverProperties)
        command.execute()
        print('{} published successfully to {}'.format(
            self.serviceConfig['serviceName'],
            self.serverProperties['host']))
