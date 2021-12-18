#!/usr/bin/env python3

import configparser
import argparse
from transmission_rpc import Client
from src.TorrentRequest import TorrentRequest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

parser = argparse.ArgumentParser(description='Sync torrent states with torrent requests DB')


config = configparser.ConfigParser()

config.read('config.ini')

if 'transmission' not in config or not config['transmission']['username'] or not config['transmission']['password']:
    raise ConnectionError('Missing required transmission config key(s).  Please check config.ini file.')

transmission_config = config['transmission']

c = Client(username=transmission_config['username'], password=transmission_config['password'])

torrents = c.get_torrents()

# TODO: Now that existing torrents are converted into TorrentRequest objects, lets sync them with firestore if necessary.
torrent_reqs = [TorrentRequest.fromTorrent(t) for t in torrents]
#print(torrent_reqs)

if 'firestore' not in config or not config['firestore']['service_account_key_path']:
    raise ConnectionError('Missing required firestore config key(s).  Please check config.ini file.')

cred = credentials.Certificate(config['firestore']['service_account_key_path'])
firebase_admin.initialize_app(cred)

db = firestore.client()

[db.collection(u'torrents').document(t_req.hash).add(t_req.toDict()) for t_req in torrent_reqs]