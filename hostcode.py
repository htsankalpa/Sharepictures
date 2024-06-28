from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory
import os

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML template as a string
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Upload Photo</title>
  </head>
  <body>
    <div class="container">
      <h1>Upload a Photo</h1>
      <form method="post" action="/upload" enctype="multipart/form-data">
        <div class="form-group">
          <label for="file">Choose file</label>
          <input type="file" name="file" id="file" class="form-control">
        </div>
        <button type="submit" class="btn btn-primary">Upload</button>
      </form>
      <h2>Uploaded Files</h2>
      <ul>
        {% for filename in files %}
          <li><a href="{{ url_for('uploaded_file', filename=filename) }}">{{ filename }}</a></li>
        {% endfor %}
      </ul>
    </div>
  </body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    # List files in the upload folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    return redirect(request.url)

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
