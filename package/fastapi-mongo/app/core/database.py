# from pymongo import MongoClient, IndexModel, ASCENDING
from motor.motor_asyncio import AsyncIOMotorClient
from ..utils.envutils import Environment

env = Environment()


client = AsyncIOMotorClient(env.MONGO_URI)

db = client["<database_name>"]

user_collection = db["users"]

otp_collection = db["otp"]

# Create a TTL(Time to live) index on the 'expires_on' field that means after the 30 sec of the value is set for the 'expires_on' field, the document will be deleted.
index = [("expires_on", 1)]
otp_collection.create_index(index, expireAfterSeconds=30)
