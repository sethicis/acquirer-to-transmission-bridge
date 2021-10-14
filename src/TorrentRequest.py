from __future__ import annotations
from datetime import datetime
from transmission_rpc.torrent import Torrent

from .Enums import TorrentRequestStatus, TorrentType

class TorrentRequest:
    def __init__(
        self,
        hash: str,
        status: TorrentRequestStatus,
        type: TorrentType = None,
        id: int = None,
        name: str = None,
        description: str = None,
        target_name: str = None,
        computed_name: str = None,
        cur_dir: str = None,
        dest_dir: str = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        self.hash = hash
        self.status = status
        self.type = type
        self.id = id
        self.name = name
        self.description = description
        self.target_name = target_name
        self.computed_name = computed_name
        self.cur_dir = cur_dir
        self.dest_dir = dest_dir
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

    def __str__(self) -> str:
        return (
        f'{self.__class__}\n'
        f'hash: {self.hash}\n'
        f'status: {self.status}\n'
        f'type: {self.type}\n'
        f'id: {self.id}\n'
        f'name: {self.name}\n'
        f'description: {self.description}\n'
        f'target_name: {self.target_name}\n'
        f'computed_name: {self.computed_name}\n'
        f'cur_dir: {self.cur_dir}\n'
        f'dest_dir: {self.dest_dir}\n'
        f'created_at: {self.created_at}\n'
        f'updated_at: {self.updated_at}\n'
        )
