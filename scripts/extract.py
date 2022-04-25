import spotipy
from pprint import pprint

TRACK_FEATURES = [
    "id",
    "name",
    "popularity",
    "duration_ms",
    "preview_url"
    ]

AUDIO_FEATURES = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo"]

def get_track_data(track_name, artist_name, sp,
    features=TRACK_FEATURES):
  try:
    query=f"artist:{artist_name} "\
          f"track:{track_name}"
    search = sp.search(q=query, type="track")
    track_data = search['tracks']['items'][0]
    return {key:val for key, val in
        track_data.items() if key in
        features}
  except:
    return None

def get_track_features(track_id, sp, features=AUDIO_FEATURES):
  try: 
    track_features = sp.audio_features([track_id])[0]
    return {key:val for key, val in
        track_features.items() if key in
        features}
  except:
    return None
