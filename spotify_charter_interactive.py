import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import os

# 環境変数から認証情報を取得
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# 必要なスコープ (適宜変更)
SCOPE = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
REDIRECT_URI = "http://localhost:8888/callback"  # ローカル開発用リダイレクト URI
# 認証オブジェクト (Authorization Code フロー)
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE,
                        cache_path=".cache")  # キャッシュを利用

# Spotify API クライアント作成
sp = spotipy.Spotify(auth_manager=sp_oauth)
# playlist id which is string after playlist/ on URL
playlist_id = '5tSbO6M5AT7r91ytDd4nNP'

# 1-> continue while, 0 -> exit while
exit_code = 1
# number of extracted track
n = 0


def is_base62(s: str) -> bool:
    """入力文字列がBase62の文字のみで構成されているか判定"""
    return bool(re.fullmatch(r'[0-9A-Za-z]+', s))


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
        tracks, key=lambda x: x["popularity"], reverse=True)[:int(n)]

    return top_tracks


def create_new_playlist(user_id, playlist_name):
    new_playlist = sp.user_playlist_create(user_id, playlist_name)
    return new_playlist


while exit_code:
    print("Starting to extract top tracks in a playlists")

    # recieve playlist_id from standard input
    playlist_id = input("Input Playlist_ID:")
    while not is_base62(playlist_id):
        print("Playlist_ID should be Base62")
        playlist_id = input("Input Playlist_ID:")
    # recieve playlist_id from standard input
    while int(n) < 1:
        n = input("Input How many tracks are extracted (at least 1):")

    top_tracks = extract_top_n(playlist_id, n)

    # create list of track id of top tracks
    top_tracks_ids = [track["id"] for track in top_tracks]
    # get current user's id
    user_info = sp.current_user()
    user_id = user_info["id"]

    # create new playlist
    playlist_info = sp.playlist(playlist_id)
    playlist_name = playlist_info["name"]
    new_playlist_name = "Top_"+str(n)+"_"+playlist_name
    new_playlist = create_new_playlist(user_id, new_playlist_name)
    new_playlist_id = new_playlist["id"]

    # add top n tracks into the new playlist
    sp.playlist_add_items(new_playlist_id, top_tracks_ids)
    print("Done!")
    exit_code = int(
        input("Continue to extract other playlist?(0-> No, 1->Yes):"))
    while exit_code != 0 and exit_code != 1:
        exit_code = int(
            input("Continue to extract other playlist?(0-> No, 1->Yes):"))
