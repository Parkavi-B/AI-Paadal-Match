import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ---------------------------
# Spotify API Authentication
# ---------------------------
# Replace these with your own keys from https://developer.spotify.com/dashboard
CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# ---------------------------
# Mood → Tamil Song Mapping
# ---------------------------
songs = {
    "love": "Ennavale Adi Ennavale",
    "sad": "Suttrum Vizhi Chudar Thaan",
    "rain": "Mazhai Kuruvi",
    "dance": "Vaathi Coming",
    "friendship": "Musthafa Musthafa",
    "happy": "Anbe En Anbe",
    "motivation": "Aalaporan Tamizhan",
    "travel": "Kadhaippoma",
    "calm": "Maruvaarthai",
    "breakup": "Kaadhal En Kaviye"
}

# ---------------------------
# Search Spotify for a Song
# ---------------------------
def search_spotify(song_name):
    results = sp.search(q=song_name, limit=1, type="track")
    items = results["tracks"]["items"]

    if items:
        track = items[0]
        spotify_link = track["external_urls"]["spotify"]
        track_name = track["name"]
        artist = track["artists"][0]["name"]
        return track_name, artist, spotify_link

    return None, None, None

# ---------------------------
# Get Song From Mood
# ---------------------------
def get_song_from_mood(mood):
    mood = mood.lower()
    if mood in songs:
        song_name = songs[mood]
        return search_spotify(song_name)
    return None, None, None

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🎧 AI Paadal Match – Tamil Song Recommender")
st.write("Enter your mood in one word and get a Tamil song!")

mood = st.text_input("Your mood:")

if st.button("Get Song"):
    if mood.strip() == "":
        st.error("Please enter a mood (e.g., love, sad, happy).")
    else:
        track_name, artist, link = get_song_from_mood(mood)

        if link:
            st.success(f"🎵 {track_name} — {artist}")
            st.markdown(f"[▶️ Listen on Spotify]({link})")
        else:
            st.error("No song found for this mood. Try another word!")