import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotifyの認証情報
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# トラック情報の取得
track = sp.track('spotify:track:4cluDES4hQEUhmXj6TXkSo')
print(track)
