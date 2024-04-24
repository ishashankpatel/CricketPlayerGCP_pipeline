import os
import json
import googleapiclient.discovery
import pandas as pd
import s3fs
from google.cloud import storage
import requests
from google.cloud import storage

BUCKET_NAME = "cricket_stat"
SOURCE_FILE_PATH = ""
DESTINATION_BLOB_NAME = "uploaded-file.txt"
CREDENTIALS_FILE = "cricket.json"


def upload_to_gcs(bucket_name, source_file_path, destination_blob_name, credentials_file):
    # Initialize the Google Cloud Storage client with the credentials
    storage_client = storage.Client.from_service_account_json(credentials_file)

    # Get the target bucket
    bucket = storage_client.bucket(bucket_name)

    # Upload the file to the bucket
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to gs://{bucket_name}/{destination_blob_name}")


    # Replace the following variables with your specific values

   

def team():
    url = "https://cricket.sportmonks.com/api/v2.0/players?api_token=***************************&filter[country_id]=153732?include=career.tournamement_type=ODI"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    teams=json.loads(response.text)
    allteamframe=pd.DataFrame(teams['data'])
    allteamframe=allteamframe.drop('resource',axis=1)
    allteamframe.to_csv("Allteams.csv",index=False)
    upload_to_gcs(BUCKET_NAME,"Allteams.csv", "Allteams.csv", CREDENTIALS_FILE)

def player():
    playerss=[]
    df=pd.read_csv('./Allteams.csv')
    df={df['id'],df['fullname']}
    p=0
    for id,namee in df:
        ids=str(id)
        url = "https://cricket.sportmonks.com/api/v2.0/players/"+ids+"?api_token=FjyVGmqKQGSUuZXG1OiiCzAAO8gJpaVqTNE5UYA6IpmMFqHXOmQmRusIBFz5&include=career"
       
        p=p+1;
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        players=json.loads(response.text)
        
        for records in players['data'].get('career',{}):
            player_info={
                'name':namee,
                'id':records.get('player_id'),
                'type':records.get('type'),
                'bowling':records.get('bowling'),
                'batting':records.get('batting')

            }
            playerss.append(player_info)
        if p==2: break
    allplayer=pd.DataFrame(playerss)
    print(allplayer)
    # allplayer.to_csv("Players/player.csv",index=False)
    # upload_to_gcs(BUCKET_NAME,"Players/player.csv", "Players/playerstat.csv", CREDENTIALS_FILE)
    

