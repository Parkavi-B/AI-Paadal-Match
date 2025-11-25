import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load Spotify credentials from Streamlit Secrets
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))


# Load songs dictionary from musicConfig.py
from musicConfig import songs, DEFAULT_SONG

# Search Spotify for a song
def search_spotify(song_name):
    try:
        results = sp.search(q=song_name, limit=1, type="track") 
        items = results["tracks"]["items"]

        if items:
            track = items[0]
            spotify_link = track["external_urls"]["spotify"]
            track_name = track["name"]
            artist = track["artists"][0]["name"]
            return track_name, artist, spotify_link

        return None, None, None

    except Exception:
        return None, None, None


# Get Song Based on Mood
def get_song_from_mood(mood):
    mood = mood.lower()  # Accepts for case insensitivity

    if mood in songs:
        song_name = songs[mood]
        return search_spotify(song_name)

    # Fallback default song
    return search_spotify(DEFAULT_SONG)

# Streamlit UI
st.title("🎧 AI Paadal Match – Tamil Song Recommender")
st.write("Enter your mood in one word and get a Tamil song!")

def convert_to_spotify_deeplink(url):
    try:
        if "track" in url:
            track_id = url.split("track/")[1].split("?")[0]
            return f"spotify:track:{track_id}"
        return url
    except:
        return url

mood = st.text_input("Your mood:")

if st.button("Get Song"):
    if mood.strip() == "":
        st.error("Please enter a mood.")
    else:
        name, artist, link = get_song_from_mood(mood)

        if link:
            deeplink = convert_to_spotify_deeplink(link)
            st.success(f"🎵 {name} — {artist}")
            st.markdown(
                f'<a href="{deeplink}">▶️ Open in Spotify App</a>',
                unsafe_allow_html=True
            )
        else:
            st.error("Unable to fetch song from Spotify.")
