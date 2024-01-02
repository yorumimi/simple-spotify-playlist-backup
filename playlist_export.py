import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import config

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.SPOTIPY_CLIENT_ID,
                                               client_secret=config.SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=config.SPOTIPY_REDIRECT_URI,
                                               scope="playlist-read-private"))

backup_folder_path = os.path.join(os.getcwd(), 'backup')

# backupフォルダが存在しない場合は作成
if not os.path.exists(backup_folder_path):
    os.makedirs(backup_folder_path)

playlists = sp.current_user_playlists()

for playlist in playlists['items']:
    file_name = os.path.join(
        backup_folder_path, f"{playlist['name'].replace('/', '_')}.txt")

    playlist_link = playlist['external_urls']['spotify']

    tracks = sp.playlist_tracks(playlist['id'])

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"Playlist Link: {playlist_link}\n\n")
        for item in tracks['items']:
            track = item['track']
            artist_name = track['artists'][0]['name']
            track_name = track['name']
            track_link = track['external_urls']['spotify']
            file.write(f"{artist_name} - {track_name} - {track_link}\n")

    print(f"Saved {playlist['name']} tracks to {file_name}")
