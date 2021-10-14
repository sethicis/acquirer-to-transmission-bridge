#!/usr/bin/env python3

import configparser
from transmission_rpc import Client
from src.TorrentRequest import TorrentRequest

config = configparser.ConfigParser()

config.read('config.ini')

if 'transmission' not in config or not config['transmission']['username'] or not config['transmission']['password']:
    raise ConnectionError('Missing required transmission config key(s).  Please check config.ini file.')

transmission_config = config['transmission']

c = Client(username=transmission_config['username'], password=transmission_config['password'])

torrents = c.get_torrents()

print([str(TorrentRequest.fromTorrent(t)) for t in torrents])
