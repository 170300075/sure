######################################
#           Bibliotecas              #
######################################
import os
from dotenv import load_dotenv
import dotenv

import pymongo
from pymongo import MongoClient

######################################
#       Conexión con bases de datos  #
######################################
load_dotenv("./config/.env")
mongodb_uri = os.getenv("MONGODB_URI")
base_url = os.getenv("BASE_URL")

print("mongodb_uri: " + mongodb_uri, end = "\n\n")
print("base_url: " + base_url, end = "\n\n")

client = MongoClient(mongodb_uri)
db = client["sure"]