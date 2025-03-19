import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# アーティスト名で検索し、ID を取得
artist_name = "Taylor Swift"
results = sp.search(q=artist_name, type="artist", limit=1)
if not results["artists"]["items"]:
    print("アーティストが見つかりません")
else:
    artist_id = results["artists"]["items"][0]["id"]
    print(f"取得したアーティスト ID: {artist_id}")

    # 関連アーティスト取得
    try:
        related = sp.artist_related_artists(artist_id)
        print(f"\n🎵 '{artist_name}' に関連するアーティスト:")
        for idx, artist in enumerate(related["artists"][:10], start=1):
            print(f"{idx}. {artist['name']
                            } (Popularity: {artist['popularity']})")
    except Exception as e:
        print("関連アーティストの取得に失敗しました:", e)
