from flask import Flask, render_template, request, send_file
import subprocess
import os
import glob

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not url:
            return render_template('index.html', error="Введіть посилання на відео!")

        try:
            # Очистити попередні завантаження
            files = glob.glob(os.path.join(DOWNLOAD_FOLDER, "*"))
            for f in files:
                os.remove(f)

            # Завантажити відео
            output_template = os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s")
            subprocess.run(["yt-dlp", "-f", "best", "-o", output_template, url], check=True)

            # Знайти завантажений файл
            downloaded_files = glob.glob(os.path.join(DOWNLOAD_FOLDER, "*"))
            if not downloaded_files:
                return render_template('index.html', error="Не вдалося завантажити відео.")

            return send_file(downloaded_files[0], as_attachment=True)
        except subprocess.CalledProcessError:
            return render_template('index.html', error="Помилка при завантаженні через yt-dlp.")
        except Exception as e:
            return render_template('index.html', error="Інша помилка: " + str(e))

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    app.run(debug=True)
