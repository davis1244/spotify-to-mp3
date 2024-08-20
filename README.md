# spotify-to-mp3
This Python app lets users download Spotify playlists as MP3s to their desktop. It uses Spotipy for Spotify API access, yt-dlp to download and convert tracks from YouTube, and tkinter for a simple GUI. Users input playlist names, and the app downloads the tracks into a designated folder on their desktop.


Here’s a `README.md` file for your project:

---

# Spotify Playlist to MP3 Downloader

This Python application allows you to download Spotify playlists as MP3 files directly to your desktop. The app features a simple graphical user interface (GUI) where you can input the name of a playlist, and it handles the rest by downloading tracks from YouTube.

## Features

- **Spotify Integration**: Authenticates with Spotify to access your playlists.
- **YouTube Downloading**: Downloads and converts tracks from YouTube to MP3 format.
- **Organized Downloads**: Saves MP3 files in a dedicated folder on your desktop.

## Requirements

- Python 3.x
- `spotipy`
- `yt-dlp`
- `tkinter` (comes with Python)
- `ffmpeg` (for audio conversion)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/spotify-playlist-downloader.git
   cd spotify-playlist-downloader
   ```

2. **Install dependencies**:
   ```bash
   pip install spotipy yt-dlp
   ```

3. **Install FFmpeg**:
   - On macOS:
     ```bash
     brew install ffmpeg
     ```
   - On Windows, download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your PATH.

4. **Configure Spotify API credentials**:
   - Create a Spotify Developer account and create an app.
   - Get your `client_id`, `client_secret`, and set a redirect URI (`http://localhost:8888/callback`).
   - Replace the placeholders in the script with your credentials.

## Usage

1. **Run the script**:
   ```bash
   python main.py
   ```

2. **Enter the playlist name** in the GUI and click "Download".

3. The tracks will be downloaded as MP3 files to a `SpotifyDownloads` folder on your desktop.

## Code Overview

### Step 1: Authentication with Spotify

This section sets up the connection to Spotify's API using OAuth, allowing access to your playlists:

```python
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="http://localhost:8888/callback",
    scope="user-library-read playlist-read-private"
))
```

### Step 2: Download a Single Track

The `download_track` function downloads a track from YouTube based on the track's name and artist:

```
def download_track(track_name, artist_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    download_folder = os.path.join(desktop_path, "SpotifyDownloads")
    os.makedirs(download_folder, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_query = f'{track_name} {artist_name} lyrics'
        ydl.download([f"ytsearch:{search_query}"])
```

### Step 3: Download an Entire Playlist

The `download_playlist` function retrieves and downloads all tracks in a Spotify playlist:

```
def download_playlist():
    playlist_name = playlist_entry.get()
    try:
        playlists = sp.current_user_playlists()
        playlist_id = None
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                playlist_id = playlist['id']
                break

        if not playlist_id:
            messagebox.showerror("Error", "Playlist not found!")
            return

        tracks = sp.playlist_tracks(playlist_id)
        for item in tracks['items']:
            track_name = item['track']['name']
            artist_name = item['track']['artists'][0]['name']
            download_track(track_name, artist_name)

        messagebox.showinfo("Download", f"Finished downloading playlist: {playlist_name}")

    except Exception as e:
        messagebox.showerror("Error", str(e))
```

### Step 4: Setting Up the GUI

The GUI allows users to input a playlist name and initiate the download process:

```
app = tk.Tk()
app.title("Spotify Playlist Downloader")

tk.Label(app, text="Enter Playlist Name:").pack()
playlist_entry = tk.Entry(app)
playlist_entry.pack()
tk.Button(app, text="Download", command=download_playlist).pack()

app.mainloop()
```

## Troubleshooting

  - Ensure `ffmpeg` is correctly installed and accessible in your system's PATH.
  - Verify Spotify API credentials are accurate and the playlist name is correct.

## License

  This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

You can replace `yourusername` with your actual GitHub username, and customize the details as needed.
