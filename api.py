from flask import Flask
from flask import request
from flask import jsonify

from object_detection import ObjectDetection

# Instantiate the object detector
object_detector = ObjectDetection()

# Instantiate Flask
app = Flask(__name__)


@app.route('/detect_objects', methods=['GET', 'OPTIONS'])
def detect_obejcts():
    json_args = request.args
    json_resp = {
        'success': None,
        'error': None,
        'labels': None,
    }
    if 'url' not in json_args:
        # User has not provided a valid request
        # return an informative error message and status code 400
        json_resp.update({'success': False, 'error': 'No parameter `url` supplied in request.'})
        status_code = 400
    else:
        # User has supplied valid `url` parameter, but we still need to validate it's content
        uri = json_args['url']
        try:
            labels = object_detector.get_objects_of_interest_from_uri(uri)
            json_resp.update({'success': True, 'labels': labels})
            status_code = 200
        except Exception as e:
            # Request failed for unknown reason (probably an invalid URL or invalid data). Return status code 400
            json_resp.update({'success': False, 'error': e.message})
            status_code = 400
    # Return the default/updated form values
    resp = jsonify(json_resp)
    resp.status_code = status_code
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')
