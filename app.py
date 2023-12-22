from pytube import YouTube
from flask import Flask, session, url_for, send_file, render_template, redirect, request
from io import BytesIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_secret_key"

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        session["link"] = request.form.get("url")
        url = YouTube(session["link"])
        url.check_availability()
        return render_template("download.html", url=url)

    return render_template('index.html')


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
