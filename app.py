from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = '/tmp' # Render වගේ තැන් වලදී /tmp පාවිච්චි කිරීම වඩාත් සුදුසුයි

@app.route('/')
def index():
    return "Backend is Running!"

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url: return "URL එකක් නැත!"

    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp4'
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()
