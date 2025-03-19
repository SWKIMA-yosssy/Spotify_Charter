import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotifyの認証情報
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
REDIRECT_URI = "http://localhost:8888/callback"  # 安全なリダイレクト URL
SCOPE = "playlist-modify-public"  # プレイリストの作成・編集に必要なスコープ

# To extract top 100 on a specific playlist
# playlist id which is string after playlist/ on URL
playlist_id = '0DBFQTRWGvV9VCoKuwdNXq'
# artist id which is string after artist/ on URL
artist_id = '49GY4uPAwdlk5lSGtfKWYl'


def get_playlist_tracks(playlist_id):
    """
    playlist_idに格納されたプレイリストの楽曲をすべて返す関数
    """
    tracks = []
    results = sp.playlist_tracks(playlist_id)

    while (results):
        for item in results["items"]:
            track = item["track"]
            if track:
                tracks.append({
                    "id": track["id"],
                    "name": track["name"],
                    "artist": ", ".join(artist["name"] for artist in track["artists"]),
                    "popularity": track["popularity"]
                })

        results = sp.next(results)

    return tracks


def extract_top_n(playlist_id, n):
    """
    与えられたplsylist_idのプレイリストのうち人気度上位n位の楽曲をランキングにして返す
    """

    # get the all playlist's tracs
    tracks = get_playlist_tracks(playlist_id)
    # extract top 100 tracks's list
    top_tracks = sorted(
        tracks, key=lambda x: x["popularity"], reverse=True)[:n]

    return top_tracks


def create_new_playlist(user_id, playlist_name):
    new_playlist = sp.user_playlist_create(user_id, playlist_name)
    return new_playlist


top_tracks = extract_top_n(playlist_id, 50)

# create list of track id of top tracks
top_tracks_ids = [track["id"] for track in top_tracks]
# get current user's id
user_info = sp.current_user()
user_id = user_info["id"]

# create new playlist
playlist_info = sp.playlist(playlist_id)
playlist_name = playlist_info["name"]
new_playlist_name = "Top_100_"+playlist_name
new_playlist = create_new_playlist(user_id, new_playlist_name)
new_playlist_id = new_playlist["id"]

# add top n tracks into the new playlist
sp.playlist_add_items(new_playlist_id, top_tracks_ids)
print("Done!")
