from pytubefix import YouTube
from pytubefix.cli import on_progress

def download_video(url, resolution='highest'):
    try:
        yt = YouTube(url, on_progress_callback = on_progress)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        if resolution == 'highest':
            selected_stream = stream.first()
        else:
            selected_stream = stream.filter(res=resolution).first()
        if selected_stream:
            print(f"Downloading: {yt.title}")
            selected_stream.download(output_path=f"C:/Code Projects/Trash Detection/data/videos/")
            print(f"Download complete: {yt.title}")
        else:
            print(f"No stream found with resolution: {resolution}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_video(video_url)
