import motor.motor_asyncio
import os

client: motor.motor_asyncio.AsyncIOMotorClient = None
db = None


async def connect_db():
    global client, db
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client[os.getenv("DB_NAME", "taskflow")]
    print("Connected to MongoDB")


async def close_db():
    if client:
        client.close()
        print("MongoDB connection closed")


def get_db():
    return db
