from tests.utils import (
    get_gcloud_bucket_test_data,
    get_object_detection_labels,
    get_objects_of_interest_from_file_name
)
from tests.mock.web_urls import WEB_URLS
from config import FLASK_SERVER_URL, OBJECTS_OF_INTEREST

from sklearn.metrics import precision_recall_fscore_support


GCLOUD_TEST_DATA = get_gcloud_bucket_test_data()

if __name__ == '__main__':
    # This file is used to get a report on how well the classification model performed,
    # with respect to the objects of interest we were looking for
    true = []
    predicted = []

    objects_of_interest_lookup = {}.fromkeys(OBJECTS_OF_INTEREST)
    # We get metrics for each class to see on which images our algorithm performs poorly
    ooi_prediction_map = {}.fromkeys(OBJECTS_OF_INTEREST)
    for k in ooi_prediction_map:
        ooi_prediction_map[k] = {'predicted': [], 'true': []}
    for labels_str, url in GCLOUD_TEST_DATA + WEB_URLS:
        true_labels_dict = {}.fromkeys(get_objects_of_interest_from_file_name(labels_str))
        # Filter out true labels which aren't in objects of interest
        true_labels_dict = {k: v for k, v in true_labels_dict.items() if k in objects_of_interest_lookup}

        resp = get_object_detection_labels(url, FLASK_SERVER_URL)
        labels = resp.json()['labels']
        for k, v in labels.items():
            if v is True and k in true_labels_dict:
                ooi_prediction_map[k]['predicted'].append(1)
                ooi_prediction_map[k]['true'].append(1)
            elif v is True and k not in true_labels_dict:
                ooi_prediction_map[k]['predicted'].append(1)
                ooi_prediction_map[k]['true'].append(0)
            elif v is False and k in true_labels_dict:
                ooi_prediction_map[k]['predicted'].append(0)
                ooi_prediction_map[k]['true'].append(1)
            else:
                # v is False and k not in true_label_dict
                ooi_prediction_map[k]['predicted'].append(0)
                ooi_prediction_map[k]['true'].append(0)

    output_str = ''
    for k, v in ooi_prediction_map.items():
        p,r,f,s = precision_recall_fscore_support(v['true'], v['predicted'])
        output_str += 'Key: {}, precision: {}, recall: {}, f1: {}, support: {}\n'.format(k, str(p), str(r), str(f), str(s))

    print('----Classification report----\n')
    print(output_str)
