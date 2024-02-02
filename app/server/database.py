import certifi
from pymongo import MongoClient

atlas_connection_string = "mongodb+srv://sayantan1413:1234@cluster0.iplw4go.mongodb.net/ecommerce?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(atlas_connection_string, tlsCAFile=certifi.where())

# Access the 'ecommerce' database or create it if it doesn't exist
db = client.get_database("ecommerce")

# Define collections
products_collection = db["products"]
orders_collection = db["orders"]