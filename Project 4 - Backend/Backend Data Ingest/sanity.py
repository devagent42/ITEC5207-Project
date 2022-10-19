import csv
from elasticsearch import Elasticsearch
import os
import json
import pandas as pd
import uuid
es = Elasticsearch("http://es01:9200")
print ("If there is something that is printed after this and it does not fail, then the Elastic database works.")
print (es.info())