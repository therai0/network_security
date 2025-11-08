
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()
mongo_db_url = os.getenv('MONGO_DB_URL')


# Create a new client and connect to the server
client = MongoClient(mongo_db_url, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)