import os
from flask import Flask, redirect, request, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import serial

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'dev/ttyUSB0'

UPLOAD_FOLDER = '/Users/rr37653/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'nc'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index(): pass

@app.route('/ace')
@app.route('/ace/<prog>')
def ace(prog):
	with open(os.path.join(app.config['UPLOAD_FOLDER'], prog), "r") as f:
		content = f.read()
	return render_template('ace.html', gcode=content, name=prog)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == "POST":
		if 'file' not in request.files:
			flash('no file part')
			return redirect(request.url)

		file = request.files['file']

		if file.filename == '':
			flash('no selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#return redirect(url_for('uploaded_file', filename=filename))
			return redirect(url_for('ace', prog=filename))

	return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('send', methods=['POST'])
def send():
	if request.method == "POST":

	else:
		return redirect(url_for('upload'))
