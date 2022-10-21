import csv
from elasticsearch import Elasticsearch
import os
import json
import pandas as pd
import uuid
es = Elasticsearch("http://es01:9200")
input_folder = "/opt/input/"

# get all the files in the input directory
data_files = []
for root, dirs, files in os.walk(input_folder):
    for name in files:
        data_files.append(os.path.join(root, name))

# Define an Elastic index mapping, to force the location field to be a "geo_point", which is a Elastic/Kibana specific field that can be plotted on the internal map in Kibana. Required.
mapping = {
    "mappings": {
        "properties": {
            "location": {
                "type": "geo_point"
            }
        }
    }
}

# create the indexs with teh specific mapping.
datasets_with_geo = ["data_red_light","data_collison","data_speed_camera"]
for dataset_name in datasets_with_geo:
    response = es.indices.create(
        index=dataset_name,
        body=mapping,
        ignore=400 # ignore 400 already exists code
    )

# add data from the CSVs to Elastic
datasets_with_geo_lowercase = ["collison","speed_camera"]
datasets_with_geo_uppercase = ["red_light"]
for file in data_files:
    name = file.split("/")[3].split(".")[0]
    tmp =  {}
    with open(file,'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #this if can be removed with further data cleaning.
            if name in datasets_with_geo_lowercase:
                tmp = {
                    "dataset":name,
                    "data":row,
                    "location":{
                        "lat":float(row["Latitude"]),
                        "lon":float(row["Longitude"])
                    }
                }
            elif name in datasets_with_geo_uppercase:
                tmp = {
                    "dataset":name,
                    "data":row,
                    "location":{
                        "lat":float(row["LATITUDE"]),
                        "lon":float(row["LONGITUDE"])
                    }
                }
            # not everything has GPS coordinates (weather data)    
            else:
                tmp = {
                    "dataset":name,
                    "data":row,
                }
            resp = es.index(index="data_"+name,document=tmp)
