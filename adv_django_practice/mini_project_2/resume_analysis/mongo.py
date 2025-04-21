from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)

db = client['resume_analyzer']

collection = db['resume_storage']
