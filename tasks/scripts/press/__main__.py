#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''ArcGIS Press

Usage:
  press <json> <server> [--overwrite]
  press (-h | --help)

Options:
  -h --help     Show this screen.
'''

import json
import sys
from arcgispress import Press
from docopt import docopt


def main():
    arguments = docopt(__doc__)

    serviceConfig = json.loads(arguments['<json>'])
    serverProperties = json.loads(arguments['<server>'])

    Press(serviceConfig, serverProperties)

    return 0

if __name__ == '__main__':
    sys.exit(main())
