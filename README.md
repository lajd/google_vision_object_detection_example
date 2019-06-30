# Flask API for Google Vision Object Detection
- Example Flask API which uses the google vision API for object detection. The google vision API returns label/confidence scores for objects in an image, whereas the provided Flask API only returns whether objects-of-interest are found in the image. An object-of-interest is said to be found if its confidence score is greater than the threshold argument.

The Flask API receives a GET request with the `url` argument (which corresponds to an image file from a web resource or a gcloud storage bucket). The URL is is sent to the vision API, where a response containing label/confidence scores is returned. We check the response for keywords associated with our objects-of-interest (in the example, they are `Car`, `Pedestrian`, `Traffic_light`). If the response returned from the vision API contains these keywords, and the confidence score is greater than a threshold (eg. 0.9), then we mark the object-of-interest as found in the image. 

## Usage
To be usable, you must place the path to your json crendentials (corresponding to your service account for gcloud's vision API) into the config.py file. In addition, indicate the OBJECTS_OF_INTEREST which you're interested in finding.

## Limitations
This is just an example of using the vision API, and doesn't take into account it's full range of features. A particular limitation is that we look for whether the exact strings in OBJECTS_OF_INTERST (OOIs) are found in the json response from the vision API, and so we need to ensure that the OOIs are of the same form returned by the vision API. A more robust system would allow for word/phrase similarity to be taken into account, for example, the vision API may identify objects such as (Jeep, Woman, Road, Lights), whereas the OOIs are (Car, Pedestrian, Traffic_light). In this case, there will be no matches. By computing word embeddings and identifying similar words, we could create a more robust system.

