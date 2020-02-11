#!/usr/bin/env python

import socket
import time

from decouple import config

port = config("POSTGRES_PORT", default=5432, cast=int)
host = config("POSTGRES_HOST", default='postgres')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except socket.error as ex:
        print('Waiting for postgres ...')
        time.sleep(0.1)
