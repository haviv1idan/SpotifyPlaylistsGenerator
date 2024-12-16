import pandas as pd

from functools import lru_cache

@lru_cache
def get_universal_top_spotify_songs() -> pd.DataFrame:
    with open('universal_top_spotify_songs.csv', 'r') as file:
        return pd.read_csv(file)
    
df: pd.DataFrame = get_universal_top_spotify_songs()

@lru_cache
def get_artists() -> list[str]:
    artists = set()
    for artists_item in df['artists'].fillna('Unknown Artist'):
        for artist in artists_item.split(','):
            if artist in artists:
                continue
            else:
                artists.add(artist)

    return artists