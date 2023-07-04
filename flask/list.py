import os
from flask import Flask, flash, request, redirect, url_for
from flask import Flask, send_from_directory, render_template 
from werkzeug.utils import secure_filename
import shutil
from PIL import Image
from datetime import date
import json

UPLOAD_FOLDER = 'static/photo'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    return "route test"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            dict = {"name" : filename, "date" : str(date.today())}
            

            with open("photos.json") as f:
                lines = list(f)  
                photos_list = ''.join(lines) 
                photos_list_dict = json.loads(photos_list)
                photos_list_dict["images"].append(dict)
                photos_list_dict["images_total"]+=1
                print(photos_list_dict)

            with open("photos.json", "w") as f:
                print(json.dumps(photos_list_dict), file=f)

            return redirect('/resized/400/' + filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route("/gallery/<width>")
def make_gallery(width):
    
    photos_list = os.listdir(path = 'static/photo')
    icons = []

    for photo in photos_list:
        icon = resize_photo(photo, width)
        icon = "../" + icon
        icons.append(icon)
        
    html = render_template("index.html", icons = icons) 
    return html

@app.route('/resized/<width>/<filename>')
def resized(filename, width):
    address_photo = resize_photo(filename, width)
    return "<img src = /" + address_photo + ">"

def resize_photo(filename, width):

    address_photo = "static/photo/" + filename

    im = Image.open(address_photo)

    ext = filename.split('.')[-1]
    name = filename.split('.')[0]
    local_resized_address = name + "_w_" +  str(width) + "." + ext
    resized_address = "static/resized/" + local_resized_address

    photos = os.listdir(path = "static/resized/")

    if not (local_resized_address in photos):
        old_width = im.size[0] 
        old_height = im.size[1] 

        width = int(width)
        height = int(width * old_height/old_width)
        size = (width, height)

        #resize image 
        out = im.resize(size)
    
        out.save(resized_address)

        print("resizing to " +  str(width))

    return resized_address

if __name__ == "__main__":
    app.run('0.0.0.0', 3010, debug = True)