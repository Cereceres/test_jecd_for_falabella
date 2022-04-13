The project consist in two main components

    Cloud Function
    Cloud Run Service

The flow in to upload a file to Cloud Storage in process the file with Cloud Service what is a 
service what get the Data from Cloud Storage and using Pandas Data Frame process the csv file
and upload the data processed to Cloud Storage again.


    Write Row Data -> [Cloud Storage] - Triggers -> [Cloud Function] - Publish -> [PubSub] - Push ->  [Cloud Run Service] -> Write Processed csv -> [Cloud Storage]

# Deploy

To deploy the cloud function:

    cd pub_storage_content 
    gcloud functions deploy --env-vars-file .env.yaml test_gcp 

To deplot the cloud run service:

    cd subs_parser_content 
    gcloud run deploy
