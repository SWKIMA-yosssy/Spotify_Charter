import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 環境変数から認証情報を取得
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8888/callback"  # ローカル開発用リダイレクト URI

# スコープ設定 (適宜変更)
SCOPE = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"

# 認証オブジェクト (Authorization Code フロー)
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE,
                        cache_path=".cache")  # キャッシュを利用

# Spotify API クライアント作成
sp = spotipy.Spotify(auth_manager=sp_oauth)

# 認証したユーザー情報を取得
user = sp.current_user()
print(f"ログインユーザー: {user['display_name']} ({user['id']})")

# アクセストークンを取得 (必要に応じて利用)
token_info = sp_oauth.get_cached_token()
if token_info:
    print("アクセストークン取得成功！")
    print("Access Token:", token_info["access_token"])
else:
    print("アクセストークン取得失敗")
