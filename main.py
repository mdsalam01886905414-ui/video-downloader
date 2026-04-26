import flet as ft
import yt_dlp
import os
import threading

DOWNLOAD_PATH = "/storage/emulated/0/DCIM/SocialMediaDownloads"

def main(page: ft.Page):
    page.title = "Video Downloader Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.padding = 20

    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    status_text = ft.Text("Ready...", size=14)
    progress = ft.ProgressBar(width=350, value=0)

    url_input = ft.TextField(
        hint_text="Paste video URL here...",
        width=350
    )

    quality_dropdown = ft.Dropdown(
        width=350,
        options=[
            ft.dropdown.Option("best"),
            ft.dropdown.Option("720"),
            ft.dropdown.Option("480"),
            ft.dropdown.Option("360"),
        ],
        value="best"
    )

    def download(mode):
        url = url_input.value.strip()
        if not url:
            status_text.value = "❌ URL দাওনি!"
            page.update()
            return

        status_text.value = "⏳ Downloading..."
        progress.value = None
        page.update()

        def task():
            try:
                opts = {
                    "outtmpl": os.path.join(DOWNLOAD_PATH, "%(title)s.%(ext)s"),
                    "quiet": True,
                    "no_warnings": True,
                }

                if mode == "audio":
                    opts["format"] = "bestaudio/best"
                    opts["postprocessors"] = [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }]
                else:
                    quality_map = {
                        "best": "bestvideo+bestaudio/best",
                        "720": "bestvideo[height<=720]+bestaudio/best",
                        "480": "bestvideo[height<=480]+bestaudio/best",
                        "360": "bestvideo[height<=360]+bestaudio/best",
                    }
                    opts["format"] = quality_map.get(
                        quality_dropdown.value, "bestvideo+bestaudio/best"
                    )
                    opts["merge_output_format"] = "mp4"

                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])

                status_text.value = "✅ Download Complete!"
                progress.value = 1

            except Exception as e:
                status_text.value = f"❌ Error: {str(e)[:50]}"
                progress.value = 0

            page.update()

        threading.Thread(target=task).start()

    page.add(
        ft.Column(
            [
                ft.Text("📥 Video Downloader Pro", size=24, weight="bold"),
                url_input,
                quality_dropdown,
                ft.ElevatedButton(
                    "📥 Download Video",
                    on_click=lambda e: download("video"),
                    width=350
                ),
                ft.ElevatedButton(
                    "🎵 Download MP3",
                    on_click=lambda e: download("audio"),
                    width=350
                ),
                progress,
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
