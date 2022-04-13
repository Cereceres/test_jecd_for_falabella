import os
from threading import Event
from google.cloud import storage, pubsub_v1
import csv
import pandas as pd
import base64
import os
from io import StringIO

storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()


def test_gcp(event, context):
    topic_path = publisher.topic_path(
        os.getenv('GOOGLE_CLOUD_PROJECT'), os.getenv('PUB_SUB_TOPIC_NAME')
    )
    print("topic_path ", topic_path)
    future = publisher.publish(
        topic_path,
        event['name'].encode('utf-8'),
        bucket_name=event['bucket'],

    )
    future.result()
