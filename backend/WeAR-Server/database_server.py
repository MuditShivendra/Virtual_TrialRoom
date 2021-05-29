from flask import Flask, request, send_from_directory, flash, redirect, url_for
import base64
import time
import socket
import sqlite3
import json
import os
from shift_and_scale import preprocess
import werkzeug.utils 
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploaded_videos'
RESIZED_VIDEO_FOLDER = 'resized_videos'
JSON_2D_OUTPUT = 'json_files'
ALLOWED_EXTENSIONS = {'mp4'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_to_db(username, two_d_output_path, three_d_output_path, videoname):
	conn = sqlite3.connect('WeAR.db')
	cur = conn.cursor()
	query = f'insert into user_files values ("{username}", "{videoname}", "{two_d_output_path}", "{three_d_output_path}");'
	cur.execute(query)
	conn.commit()
	conn.close()



def pose_estimation_2D(filename):
	# filename = os.path.splittext(filename)[0]
	filename = filename[:-4]
	os.system(f'ffmpeg -i {UPLOAD_FOLDER}/{filename}.mp4 -vf scale=480:848 {RESIZED_VIDEO_FOLDER}/{filename}_480_848.mp4')
	
	os.system(f'mkdir {JSON_2D_OUTPUT}/{filename}')
	os.system(f'pose_estimation_scripts/two_d.sh {RESIZED_VIDEO_FOLDER}/{filename}_480_848.mp4 {JSON_2D_OUTPUT}/{filename}')
	return f'{JSON_2D_OUTPUT}/{filename}'


def pose_estimation_3D(filepath):
	print("hello")
	print(f'pose_estimation_scripts/three_d.sh {filepath}')
	os.system(f'pose_estimation_scripts/three_d.sh {filepath}')
	os.system(f'mv ../3d-pose-baseline/maya/2d_data.json {JSON_2D_OUTPUT}/{filepath}_2d.json')
	os.system(f'mv ../3d-pose-baseline/maya/3d_data.json {JSON_2D_OUTPUT}/{filepath}_3d.json')
	os.system(f'rm -rf {filepath}')
	# TODO remove videos
	return (f'{JSON_2D_OUTPUT}/{filepath}_2d.json', f'{JSON_2D_OUTPUT}/{filepath}_3d.json')


@app.route('/login', methods=['GET', 'POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	# role = request.form['role']
	conn = sqlite3.connect('WeAR.db')
	cur = conn.cursor()
	cur.execute("SELECT password from Users WHERE username='bakwas'")
	res = cur.fetchone()
	print(res)
	conn.close()
	if password == res[0]: #and role == res[1]:
		return "success"
	else:
		 return "failure"


@app.route('/register', methods=['POST'])
def register():
	username = request.form['username']
	password = request.form['password']
	role = request.form['role']
	screenheight = request.form['screenheight']
	screenwidth = request.form['screenwidth']
	print(username, password, role, screenheight, screenwidth)
	conn = sqlite3.connect('WeAR.db')
	cur = conn.cursor()
	query = f'insert into Users (`username`, `password`, `screenheight`, `screenwidth`) values ("{username}", "{password}", "{screenheight}", "{screenwidth}");'
	cur.execute(query)
	conn.commit()
	conn.close()

	return "success"


@app.route('/upload_video', methods=['POST'])
def upload_video():
	if request.method == 'POST':
		username = request.form['username']
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return "No File"
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return "No File"
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			# print(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			output_2D = pose_estimation_2D(filename)
			res = pose_estimation_3D(output_2D)
			preprocess(res[0], res[0].split('/')[-1])
			# preprocess(os.path.join(app.config['UPLOAD_FOLDER']), filename)
			add_to_db(username, res[0], res[1], filename)
			return "success"

	return "nani!"


@app.route('/download_ready', methods=['GET', 'POST'])
def get_3D_points():
	username = request.form['username']
	print(request.form)
	print(username)
	conn = sqlite3.connect('WeAR.db')
	cur = conn.cursor()
	cur.execute('SELECT videoname, json2Dfilename, json3Dfilename FROM Users WHERE username=?', (username, ))
	row = cur.fetchone()
	print(row)
	if row:
		print("VideoFileName", row[0], "Json2DFileName", row[1], "Json3DFileName", row[2])
		return json.dumps({"VideoFileName": row[0], "Json2DFileName": row[1], "Json3DFileName": row[2]})
		# return json.dumps({"VideoFileName": "test.txt", "Json2DFileName": "test.txt", "Json3DFileName": "test.txt"})
	else:
		return "NotReady"
	
	conn.close()


@app.route('/return_files/<path:subpath>', methods=['GET', 'POST'])
def return_files(subpath):
	try:
		print(subpath.split('/'))
		return send_from_directory(directory=subpath.split('/')[0], filename=subpath.split('/')[1])
		# return send_from_directory(directory="Videos", filename="test.txt")
	except Exception as e:
		return str(e)


if __name__ == '__main__':
	app.run("0.0.0.0", debug=True)