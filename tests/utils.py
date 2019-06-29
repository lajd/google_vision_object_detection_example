import requests

from config import PATH_TO_CREDENTIALS, TEST_GCLOUD_BUCKET

from google.cloud import storage

assert PATH_TO_CREDENTIALS is not None, "Must supply path to service account json credentials"


def get_gcloud_bucket_test_data(bucket_name=TEST_GCLOUD_BUCKET):
    """ This bucket contains publicly-accessible test data

    # The test data are .jpg images obtained from the internet
    # eg. https://storage.googleapis.com/public_classification_images/car_1.jpg
    """

    storage_client = storage.Client.from_service_account_json(PATH_TO_CREDENTIALS)
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()
    # The name of the bucket contains label information
    google_storage_bucket_url = 'http://storage.googleapis.com/' + bucket_name + "/"
    name_url_tuples = [(blob.name, google_storage_bucket_url + blob.name) for blob in blobs]
    return name_url_tuples


def get_object_detection_labels(url, flask_server, endpoint_name='detect_objects'):
    payload = {'url': url}
    r = requests.get(flask_server + endpoint_name, params=payload)
    return r


def get_objects_of_interest_from_file_name(fname):
    # labels contained in fname are assumed to be of the form returned by the vision API,
    # and multiple labels are comma-separated.
    # eg. `Traffic_light,Pedestrian,1.jpg`
    # Any numbers are ignored (used to avoid duplicates)
    candidate_objects = fname.split(',')
    valid_objects = []
    for obj in candidate_objects:
        try:
            # This is not a valid object, just an index to avoid duplicates
            float(obj)
        except ValueError:
            # This is a valid object
            valid_objects.append(obj)
    return valid_objects


def assert_valid_response_format(resp, objects_of_interest_lookup):
    # Assert the response was successful
    assert resp.status_code == 200
    json = resp.json()
    # Assert that the json response is formatted as we expect
    assert set(json.keys()) == {'labels', 'success', 'error'}
    assert set(objects_of_interest_lookup) == set(json['labels'].keys())
    for val in json['labels'].values():
        assert isinstance(val, bool)
