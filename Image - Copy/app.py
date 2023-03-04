import requests
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder
from flask import Flask, request, jsonify, redirect
from PIL import Image
import io

app = Flask(__name__)

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
            "endpoint": 'process_image',
            "route": '/swagger.yml',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, template=swagger_template, config=swagger_config)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def apidocs():
    return redirect('/api/spec')

@app.route('/process-image', methods=['POST'])
@swag_from("swagger.yml", methods=['POST'])
def process_image():
    '''
        # Check if the request contains the necessary data
        if 'image' not in request.files or 'operations' not in request.form:
            return jsonify({'error': 'Missing image or operations data'}), 400

        # Extract the image data and operations from the request
        image_data = request.files['image'].read()
        operations = request.form['operations']

        # Check if the file extension is allowed
        if not allowed_file(request.files['image'].filename):
            return jsonify({'error': 'Invalid file type. Allowed file types are: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400

        # Convert the operations string to a list of dicts
        try:
            operations = eval(operations)
        except requests.RequestException:
            return jsonify({'error': 'Invalid operations data. Please provide a valid list of dictionaries.'}), 400

        # Process the image using the provided operations
        with io.BytesIO(image_data) as image_buffer:
            try:
                image = Image.open(image_buffer)
            except requests.RequestException:
                return jsonify({'error': 'Unable to read image data. Please provide a valid image file.'}), 400

            for operation in operations:
                if operation['name'] == 'flip':
                    if operation['axis'] == 'horizontal':
                        image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
                    elif operation['axis'] == 'vertical':
                        image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
                    else:
                        return jsonify({'error': 'Invalid flip axis. Please provide "horizontal" or "vertical".'}), 400
                elif operation['name'] == 'rotate':
                    if 'degrees' in operation:
                        image = image.rotate(operation['degrees'])
                    else:
                        return jsonify({'error': 'Missing "degrees" parameter for rotate operation.'}), 400
                elif operation['name'] == 'grayscale':
                    if 'scale' in operation and operation['scale'].lower() == 'yes':
                        image = image.convert(mode='L')
                    else:
                        return jsonify({
                            'error': 'Missing or invalid "scale" parameter for grayscale operation. Please provide "yes" '
                                     'or omit.'}), 400
                elif operation['name'] == 'resize':
                    if 'size' in operation and len(operation['size']) == 2:
                        image = image.resize(operation['size'])
                    else:
                        return jsonify({
                            'error': 'Missing or invalid "size" parameter for resize operation. Please provide a tuple of '
                                     '(width, height).'}), 400
                else:
                    return jsonify({
                        'error': 'Invalid operation name. Allowed values are: "flip", "rotate", "grayscale", "resize".'}), 400

            with io.BytesIO() as output_buffer:
                image.save(output_buffer, format='JPEG')
                processed_image_data = output_buffer.getvalue()

        # Return the processed image data
        return jsonify({'data': processed_image_data}), 200
    '''
print("This is an image processing application.")

if __name__ == '__main__':
    app.run(debug=True)
