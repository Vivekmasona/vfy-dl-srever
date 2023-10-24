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

@app.route('/download', methods=['GET'])
def download_4k_video():
    yt_url = request.args.get('url')

    try:
        yt = YouTube(yt_url)
        stream = yt.streams.filter(res="2160p").first()

        if stream:
            video_data = stream.stream_to_buffer()
            response = Response(video_data, content_type='video/mp4')
            response.headers['Content-Disposition'] = f'attachment; filename={yt.title}.mp4'
            return response
        else:
            return "No 4K video available for this URL."

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
