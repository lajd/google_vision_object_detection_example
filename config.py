# Credentials json file associated with google vision service account
# Must be added in order to run tests/launch API!
PATH_TO_CREDENTIALS = None
# Flask host
FLASK_SERVER_URL = "http://0.0.0.0:5000/"
# The objects we're interested in detecting. Must be of the same form of those returned by the google vision API
OBJECTS_OF_INTEREST = ['Car', 'Pedestrian','Traffic_light']
# Link to a google cloud bucket associated with credentials containing sample images.
TEST_GCLOUD_BUCKET = 'public_classification_images'