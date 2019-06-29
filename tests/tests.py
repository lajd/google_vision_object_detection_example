from utils import (
    get_gcloud_bucket_test_data,
    get_object_detection_labels,
    assert_valid_response_format
)
from mock.web_urls import WEB_URLS, INVALID_URL
from config import FLASK_SERVER_URL, OBJECTS_OF_INTEREST

GCLOUD_TEST_DATA = get_gcloud_bucket_test_data()


class TestObjectDetectionAPI:
    def test_valid_response_gcloud_url(self):
        # Test that the API works and returns a valid json resp
        test_url = GCLOUD_TEST_DATA[0][1]
        resp = get_object_detection_labels(test_url, FLASK_SERVER_URL)
        assert_valid_response_format(resp, OBJECTS_OF_INTEREST)

    def test_valid_response_web_url(self):
        # Test that the API works and returns a valid json resp
        test_url = WEB_URLS[0][1]
        resp = get_object_detection_labels(test_url, FLASK_SERVER_URL)
        assert_valid_response_format(resp, OBJECTS_OF_INTEREST)

    def test_invalid_url(self):
        # Test that the API errors gracefully when a bad URL is provided
        test_url = INVALID_URL[0]
        resp = get_object_detection_labels(test_url, FLASK_SERVER_URL)
        assert resp.status_code == 400
        assert resp.json()['error'] is not None

