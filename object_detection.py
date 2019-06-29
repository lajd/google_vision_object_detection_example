from config import PATH_TO_CREDENTIALS, OBJECTS_OF_INTEREST

# Imports the Google Cloud client library
from google.cloud import vision

assert PATH_TO_CREDENTIALS is not None, "Must supply path to service account json credentials"


class ObjectDetection:
    def __init__(self):
        self.gcloud_vision_client = vision.ImageAnnotatorClient.from_service_account_json(
            PATH_TO_CREDENTIALS
        )

    def get_objects_of_interest_from_uri(self, uri):
        """ Check whether the objects of interest are identified in the image corresponding to the uri
        
        Args:
            uri (str): google storage file or url
        
        Returns:
            identified_objects_of_interest (dict): dictionary specifying whether the object of interest was
                found in the image

        Raises:
            Exception if the image could not be read by the vision API
        """
        label_annotations_resp = self.get_label_annotations_from_img_uri(uri)
        if label_annotations_resp.error.code != 0:
            # There was an error when returning the request. Propagate the error message
            raise Exception(label_annotations_resp.error.message)
        else:
            # Response returned without error; continue processing
            identified_objects_of_interest = self.identify_presence_of_objects_of_interest(
                label_annotations_resp, OBJECTS_OF_INTEREST
            )
            return identified_objects_of_interest

    def get_label_annotations_from_img_uri(self, uri):
        """Detects labels in the file located in Google Cloud Storage or on the Web.

        Args:
            uri (str): Google cloud storage file or web URL

        Returns:
            label_annotations_resp (object): google cloud vision object containing the response
        """

        # Convert URL into an image
        image = vision.types.Image()
        image.source.image_uri = uri

        # Send image to server and get label/probability response
        label_annotations_resp = self.gcloud_vision_client.label_detection(image=image)
        return label_annotations_resp

    @staticmethod
    def identify_presence_of_objects_of_interest(label_annotations_resp, objects_of_interest, identified_threshold=0.9):
        """ Parse the label-annotation object into the required output format

        Output format looks for three types of objects, and is of form:
            {
                car: true,
                pedestrian: true,
                traffic_light: false
            }

        Where an object is identified as `true` iff the corresponding confidence score is greater than 0.9

        Args:
            label_annotations_resp (object): google cloud vision object
            objects_of_interest (list of str): list of objects of interest, corresponding to objects
                identifiable by the google image API
            identified_threshold (float): threshold in (0, 1) for which we mark an object as identified

        Returns:
            identified_objects_of_interest (dict): dictionary containing whether the
                objects of interest were contained in the image uri
        """
        # Initially, we haven't seen any objects of interest (default is False).
        identified_objects_of_interest = {}.fromkeys(objects_of_interest, False)
        for label_attributes in label_annotations_resp.label_annotations:
            name, score = label_attributes.description, label_attributes.score
            if name in identified_objects_of_interest and score > identified_threshold:
                # This attribute contains an object of interest, and the object score is above the cutoff threshold
                identified_objects_of_interest[name] = True
        return identified_objects_of_interest






