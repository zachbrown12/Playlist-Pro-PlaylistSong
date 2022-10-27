import os
from resources.rds_data_service import RDSDataService
from resources.songs_resource import SongsResource
from resources.playlist_resource import PlaylistResource
from resources.playlist_song_resource import PlaylistSongsResource

# DATABASE CONFIGS
class RDSDataServiceConfig:
    def __init__(self, db_user, db_pw, db_host, db_port):
        self.db_user = db_user
        self.db_pw = db_pw
        self.db_host = db_host
        self.db_port = db_port


# RESOURCES CONFIGS
class SongsResourceConfig:
    def __init__(self, data_service, collection_name):
        self.data_service = data_service
        self.collection_name = collection_name

class PlaylistResourceConfig:
    def __init__(self, data_service, collection_name):
        self.data_service = data_service
        self.collection_name = collection_name

class PlaylistSongsResourceConfig:
    def __init__(self, data_service, collection_name):
        self.data_service = data_service
        self.collection_name = collection_name


class ServiceFactory:
    def __init__(self):
        self.rds_svc_config = RDSDataServiceConfig(
            os.environ.get("DBUSER"),
            os.environ.get("DBPW"),
            os.environ.get("DBHOST"),
            os.environ.get("DBPORT")
        )
        self.rds_service = RDSDataService(self.rds_svc_config)
        # connect songs resource to rds
        self.songs_service_config = SongsResourceConfig(self.rds_service, "PlaylistPro.Song")
        self.songs_resource = SongsResource(self.songs_service_config)
        # connect playlists resource to rds
        self.playlists_service_config = PlaylistResourceConfig(self.rds_service, "PlaylistPro.Playlist")
        self.playlists_resource = PlaylistResource(self.playlists_service_config)
        # connect playlist songs resource to mongo
        self.playlistsongs_service_config = PlaylistSongsResourceConfig(self.rds_service, "PlaylistPro.PlaylistSong")
        self.playlistsongs_resource = PlaylistSongsResource(self.playlistsongs_service_config)

    def get(self, resource_name, default):
        if resource_name == "songs":
            result = self.songs_resource
        elif resource_name == "playlists":
            result = self.playlists_resource
        elif resource_name == "playlistsongs":
            result = self.playlistsongs_resource
        else:
            result = default
        return result