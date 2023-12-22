from flask import Flask, request

app = Flask(__name__)

import yt_dlp as youtube_dl

def get_mp3(video_url, destination_path="~/Music"):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url, download=False
    )

    options = {'format': 'bestaudio/best', 'keepvideo': False, 'outtmpl': f"{destination_path}/{video_info['title']}.mp3"}

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

@app.route('/MP3', methods=['GET'])
def mp3_from_url():
    video_url = request.args.get('url', '')
    destination_path = "~/Music"  # You can change this to your preferred destination path
    get_mp3(video_url, destination_path)
    return "MP3 download initiated."

if __name__ == '__main__':
    app.run(debug=True)
