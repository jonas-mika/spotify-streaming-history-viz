import spotipy

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

def get_track_data(track_name, artist_name, token):
  try:
    sp = spotipy.Spotify(auth=token)
    query=f"artist:{artist_name} "\
          f"track:{track_name}"
    search = sp.search(q=query, type="track")
    track_data = search['tracks']['items'][0]

    return track_data
  except: 
    return None

def get_track_features(track_id, token,
    features=AUDIO_FEATURES):
  try:
    sp = spotipy.Spotify(auth=token)
    track_features = sp.audio_features([trackId])[0]
    return track_features[features]
  except: 
    return None
