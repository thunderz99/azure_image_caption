import sys
import os
import json
import urllib
from PIL import Image
from flask import Flask, request, redirect, url_for
from flask import send_from_directory, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
from caption_service import CaptionService
from translation_service import TranslationService

sys.path.append(os.curdir)  # カレントファイルをインポートするための設定
UPLOAD_FOLDER = '/tmp/uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_url_path='/static', static_folder='assets/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cs = CaptionService()
ts = TranslationService()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/flask/uploader', methods=['POST'])
def upload_file():
    # check if the post request has the file part

    # create a special subfolder for the files uploaded this time
    # to avoid overwrite
    subdir = datetime.now().strftime('%Y%m%d_%H%M%S')
    current_files_dir = os.path.join(UPLOAD_FOLDER, subdir)
    os.makedirs(current_files_dir, exist_ok=True)

    upload_files = request.files.getlist('file[]')
    ret = []
    for file in upload_files:
        image = {}

        print('filename is', file.filename)
        filename = secure_filename(file.filename)
        image['filename'] = filename

        filepath = os.path.join(current_files_dir, filename)
        print('file saving to ', filepath)
        file.save(filepath)

        image['url'] = '/flask/uploads/{}/{}'.format(
            subdir, urllib.parse.quote_plus(filename))

        print('begin predict', filepath)
        caption_en, caption_ja = get_caption(filepath)
        image['result'] = caption_ja

        ret.append(image)

    return json.dumps(ret)


@app.route('/flask/uploads/<path:filepath>')
def uploaded_file(filepath):
    print("filepath is {}".format(filepath))

    filename = os.path.basename(filepath)

    if not filename:
        return ""

    path = os.path.dirname(filepath)
    print("path is {}, filename is {}".format(path, filename))

    image_folder = os.path.join(UPLOAD_FOLDER, path)
    return send_from_directory(image_folder,
                               urllib.parse.unquote_plus(filename))


@app.route('/')
def serve_index():
    return send_from_directory('assets', 'index.html')


@app.route('/<filename>', defaults={'filename': 'index.html'})
def serve_assets(filename):
    return send_from_directory('assets', filename)


def get_caption(filepath):
    print('getting caption', filepath)
    caption_en = cs.get_caption(filepath)
    caption_ja = ts.get_translation(caption_en)
    return caption_en, caption_ja


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)
