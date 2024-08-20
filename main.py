import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp
import tkinter as tk
from tkinter import messagebox

# Step 1: Authentication with Spotify
# This sets up the connection to Spotify's API using OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    #find these 3 lines below on spotify developer app on website
    client_id="057de2c74c4046cbbb8a5ea1694bba9b",
    client_secret="360c43b852e945aa94c028e29dd8f646",
    redirect_uri="http://localhost:8888/callback",
    # Permissions needed to read playlists
    scope="user-library-read playlist-read-private"
))

# Step 2: Function to download a single track from YouTube
def download_track(track_name, artist_name):
    # Get the user's Desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Create a folder on the Desktop named 'SpotifyDownloads'
    download_folder = os.path.join(desktop_path, "SpotifyDownloads")
    os.makedirs(download_folder, exist_ok=True)

    # Options for yt-dlp to download and convert the audio
    ydl_opts = {
        'format': 'bestaudio/best',  # Get the best audio quality available
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',  # Path to FFmpeg installed via Homebrew
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save files in the download folder with track title as name
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extract the audio using FFmpeg
            'preferredcodec': 'mp3',  # Convert the audio to MP3 format
            'preferredquality': '192',  # Set the quality of the MP3 file
        }],
    }

    # Search YouTube for the track and download it
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_query = f'{track_name} {artist_name} lyrics'
        ydl.download([f"ytsearch:{search_query}"])

# Step 3: Function to download an entire playlist
def download_playlist():
    playlist_name = playlist_entry.get()  # Get the playlist name from the GUI entry

    # Fetch the user's playlists from Spotify
    try:
        playlists = sp.current_user_playlists()
        playlist_id = None

        # Find the playlist ID based on the provided name
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                playlist_id = playlist['id']
                break

        if not playlist_id:
            messagebox.showerror("Error", "Playlist not found!")  # Show error if playlist is not found
            return

        # Fetch tracks in the playlist using the playlist ID
        tracks = sp.playlist_tracks(playlist_id)

        # Download each track in the playlist
        for item in tracks['items']:
            track_name = item['track']['name']
            artist_name = item['track']['artists'][0]['name']
            download_track(track_name, artist_name)

        messagebox.showinfo("Download", f"Finished downloading playlist: {playlist_name}")  # Show success message

    except Exception as e:
        messagebox.showerror("Error", str(e))  # Show any errors that occur

# Step 4: Setting up the GUI
app = tk.Tk()
app.title("Spotify Playlist Downloader")

# Label for playlist name entry
tk.Label(app, text="Enter Playlist Name:").pack()

# Text entry for the playlist name
playlist_entry = tk.Entry(app)
playlist_entry.pack()

# Button to start the download
tk.Button(app, text="Download", command=download_playlist).pack()

# Run the GUI application
app.mainloop()
