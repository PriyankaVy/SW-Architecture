import io
import os
import uuid

from flask import Flask, Response, send_file, request, render_template, jsonify
from flask_jsonrpc import JSONRPC
from werkzeug.utils import secure_filename, redirect
from PIL import Image
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder

#Defining upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

#Defining output folder path
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'outputs')

#Defining allowed files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#Defining Swagger UI Document template and configuration
swagger_template = dict(
info={
    'title': LazyString(lambda: 'My first Swagger UI document'),
    'version': LazyString(lambda: '0.1'),
    'description': LazyString(lambda:'This document depicts a Swagger UI document and implements image_process '
                                     'functionality after executing POST.'),
    },
    host=LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'image_process',
            "route": '/image_process.yml',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
#limit file size to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.json_encoder = LazyJSONEncoder
jsonrpc = JSONRPC(app, '/api')
swagger = Swagger(app, template=swagger_template, config=swagger_config)

@app.route('/apidocs')
def apidocs():
    return redirect('/apidocs/index.html?url=/api/spec')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
@swag_from("image_process.yml", methods=['POST'])
def image_process():
    # Get the image file from the request
    uploaded_img = request.files['image']

    # Get the operations to perform from the request
    operations = request.form.getlist('myOperation')

    # Save the uploaded file to disk
    filename = str(uuid.uuid4()) + secure_filename(uploaded_img.filename)
    uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Perform the image processing operations
    try:
        processed_image = process_image(filename, operations)

        # Save the processed image to a file
        processed_filename = str(uuid.uuid4()) + '.jpg'
        processed_file_path = os.path.join(app.config['OUTPUT_FOLDER'], processed_filename)
        with open(processed_file_path, 'wb') as f:
            f.write(processed_image.getvalue())

        # Create a response with the processed image
        return Response(processed_image.getvalue(), mimetype='image/jpeg')

    except Exception as e:
        #Handle errors gracefully
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'error': str(e)}), 500

def process_image(filename, operations):
    # Read the image file using Pillow
    with Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as img:

        # Apply the operations to the image in order
        for operation in operations:
            if operation == 'rotate':
                img = img.rotate(180, expand=True)
            elif operation == 'rotate_left':
                img = img.rotate(90, expand=True)
            elif operation == 'rotate_right':
                img = img.rotate(-90, expand=True)
            elif operation == 'flip_vertical':
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            elif operation == 'flip_horizontal':
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif operation == 'grayscale':
                img = img.convert('L')
            elif operation == 'resize':
                img = img.resize((int(img.width * 0.5), int(img.height * 0.5)))
            elif operation == 'thumbnail':
                img.thumbnail((128, 128))

        # Save the processed image to a bytes buffer
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Return the processed image data as a bytes buffer
        return buffer

#Validate file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # check if file exists
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # check if file extension is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'File extension not allowed'}), 400


if __name__ == '__main__':
    app.run(debug=True)

