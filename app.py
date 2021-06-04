import os
import shutil
from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask import send_from_directory
from werkzeug import secure_filename
import logging
from unicodedata import normalize


# your procesing code moudle
from cnnDet import get_result

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'bmp', 'jpeg', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 20M
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format=LOG_FORMAT)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ppt_detection', methods=['GET', 'POST'])
def upload_file():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])
    if request.method == 'POST':
        file = request.files['file'] if 'file' in request.files.keys() else None
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = normalize('NFKD', file.filename).encode('utf-8', 'ignore').decode('utf-8')
            print(filename)
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                name, ext = os.path.splitext(filename)
                num = 0
                while True:
                    filename = name + '_' + str(num) + ext
                    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                        break
                    num += 1
            app.logger.info('uploaded filename: {}'.format(filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            img_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # some processing code by your model
            get_result(img_name)
            # some processing code by your model
            res_name = os.path.join(app.config['OUTPUT_FOLDER'], 'dst.jpg')
            print(res_name)
            return render_template('index.html', frame0=img_name, frame1=res_name)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/outputs/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1800, use_reloader=False, threaded=True)
