from yt_dlp import YoutubeDL

def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "outtmpl": "downloads/%(title)s.%(ext)s"
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
