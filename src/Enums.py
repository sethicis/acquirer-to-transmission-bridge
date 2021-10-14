from enum import Enum


class TorrentRequestStatus(Enum):
    QUEUED = 1 # Queued to be added to the torrent downloads
    STOPPED = 2 # Added but not downloading
    DOWNLOADING = 3 # Actively downloading
    PENDING_REVIEW = 4 # Completed download, but requires manual review to complete
    DONE = 5 # Completed


class TorrentType(Enum):
    MOVIE = 1
    SHOW = 2 # like tv show
    OTHER = 3 # everything else
