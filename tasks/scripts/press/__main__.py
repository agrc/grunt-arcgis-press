#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''ArcGIS Press

Usage:
  press stage <ip> <username> <password> <json> [<temp_folder>]
  press upload <ip> <username> <password> <sd> <connection_file>
  press edit <ip> <username> <password> <json> [<temp_folder>]
  press publish <ip> <username> <password> <json> [<temp_folder>]
  press (-h | --help)

Options:
  -h --help     Show this screen.
'''

import json
import sys
from arcgispress import Press
from docopt import docopt
from os import getcwd
from os.path import join


def main():
    arguments = docopt(__doc__)

    credentials = {
      'username': arguments['<username>'],
      'password': arguments['<password>'],
      'host': arguments['<ip>']
    }

    config_json = arguments['<json>']
    temp_folder = arguments['<temp_folder>']
    if(config_json):
        service_config = json.loads(arguments['<json>'])

        if not temp_folder:
            temp_folder = join(getcwd(), '.temp')

        temp_folder = join(temp_folder, service_config['serviceName'])

    press = Press(credentials, temp_folder)

    if arguments['stage']:
        return press.stage(service_config)

    if arguments['upload']:
        return press.upload(arguments['<sd>'], arguments['<connection_file>'])

    if arguments['edit']:
        return press.edit(service_config)

    if arguments['publish']:
        sd, connection_file = press.stage(service_config)
        press.upload(sd, connection_file)
        press.edit(service_config)

        return

if __name__ == '__main__':
    sys.exit(main())
