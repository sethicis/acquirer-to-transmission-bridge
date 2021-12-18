from __future__ import annotations
from datetime import datetime
from logging import makeLogRecord
from transmission_rpc.torrent import Torrent

from .Enums import TorrentRequestStatus, TorrentType

class TorrentRequest(object):
    def __init__(
        self,
        hash: str,
        status: TorrentRequestStatus,
        type: TorrentType = None,
        name: str = None,
        description: str = None,
        target_name: str = None,
        computed_name: str = None,
        cur_dir: str = None,
        dest_dir: str = None,
        magnet: str = None,
        added_by: str = None, # User who added the request
        requires_review: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        self.hash = hash
        self.status = status
        self.type = type
        self.name = name
        self.description = description
        self.target_name = target_name
        self.computed_name = computed_name
        self.cur_dir = cur_dir
        self.dest_dir = dest_dir
        self.magnet = magnet
        self.added_by = added_by
        self.requires_review = requires_review
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.updated_at = updated_at if updated_at is not None else datetime.utcnow()

    @classmethod
    def fromTorrent(cls, t: Torrent) -> TorrentRequest:
        return cls(
            hash=t.hashString,
            name=t.name if t.name is not t.hashString else None,
            status=cls.__parse_torrent_status(t),
            cur_dir=t.download_dir
        )

    @staticmethod
    def __parse_torrent_status(torrent: Torrent) -> TorrentRequestStatus:
        status = torrent.status
        if status.download_pending or status.downloading:
            return TorrentRequestStatus.DOWNLOADING    
        elif status.seed_pending or status.seeding:
            return TorrentRequestStatus.PENDING_REVIEW
        else:
            return TorrentRequestStatus.STOPPED if torrent.progress != 1 else TorrentRequestStatus.PENDING_REVIEW

    @classmethod
    def fromDict(cls, source: dict) -> TorrentRequestStatus:
        return cls(
            hash=source.get('hash'),
            status=TorrentRequestStatus[dict.get('status', 'QUEUED')],
            type=TorrentType[dict.get('type')] if dict.get('type') is not None else None,
            name=dict.get('name'),
            description=dict.get('description'),
            target_name=dict.get('target_name'),
            computed_name=dict.get('computed_name'),
            cur_dir=dict.get('cur_dir'),
            dest_dir=dict.get('dest_dir'),
            magnet=dict.get('magnet'),
            added_by=dict.get('added_by'),
            requires_review=dict.get('requires_review', True),
            created_at=dict.get('created_at'),
            updated_at=dict.get('updated_at'),
        )

    def toDict(self):
        return {
            'hash' : self.hash,
            'status' : self.status,
            'type' : self.type,
            'name' : self.name,
            'description' : self.description,
            'target_name' : self.target_name,
            'computed_name' : self.computed_name,
            'cur_dir' : self.cur_dir,
            'dest_dir' : self.dest_dir,
            'magnet' : self.magnet,
            'added_by' : self.added_by,
            'requires_review' : self.requires_review,
            'created_at' : self.created_at,
            'updated_at' : self.updated_at,
        }

    def __repr__(self) -> str:
        return (
            f'TorrentRequest(\
                hash={self.hash}\
                name={self.name}\
                status={self.status}\
                type={self.type}\
                description={self.description}\
                target_name={self.target_name}\
                computed_name={self.computed_name}\
                cur_dir={self.cur_dir}\
                dest_dir={self.dest_dir}\
                magnet={self.magnet}\
                added_by={self.added_by}\
                requires_review={self.requires_review}\
                created_at={self.created_at}\
                updated_at={self.updated_at}\
            )'
        )
