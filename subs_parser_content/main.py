import os
from typing import Optional
from google.cloud import storage
import csv
import pandas as pd
from io import StringIO


import base64
import os

from flask import Flask, request


app = Flask(__name__)
storage_client = storage.Client()
target_bucket = os.getenv("BUCKET")


@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]
    is_valid_message = isinstance(
        pubsub_message, dict) and "data" in pubsub_message
    if is_valid_message:
        csv_name = base64.b64decode(
            pubsub_message["data"]
        ).decode("utf-8").strip()
        bucket_name = pubsub_message["attributes"]["bucket_name"]
        file_name = ".".join(csv_name.split(".")[0:-1])
        bucket = storage_client.get_bucket(bucket_name)
        blob_source = bucket.blob(csv_name)

        print("file ",  blob_source.download_as_bytes().decode()[0:100])

        csv_string = blob_source.download_as_bytes().decode()
        csv_contents = StringIO(csv_string)
        df = pd.read_csv(csv_contents)
        print("info ", df.info())
        df["Latitude"] = "*********"
        df["Longitude"] = "*********"
        temp_by_country = df.groupby("Country")
        bucket = storage_client.get_bucket(target_bucket)

        for country, temp_df in temp_by_country:
            blob = bucket.blob(f"{file_name}_from_{country}.csv")
            # 'text/csv'
            blob.upload_from_string(data=temp_df.to_csv())
    return ("", 204)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080
    app.run(host="127.0.0.1", port=PORT, debug=True)
