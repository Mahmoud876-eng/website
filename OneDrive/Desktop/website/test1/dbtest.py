from pymongo import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://mahmoudmalek2004:ianDQZpjFlr9QctF@cluster0.f4icykw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Connect to MongoDB server
client = MongoClient(uri, server_api=ServerApi('1'))

# Create a database
db = client["user_database"]

# Create a collection
users_collection = db["users"]

# Example user data

# Insert user data into the collection

# Retrieve and print all inserted data
all_users = users_collection.find()
#for user in all_users:

#    print(f"Inserted User: {user}")
user_with_id_1 = users_collection.find_one({"username": "example_user"})
if user_with_id_1 and 'email' in user_with_id_1:
    print(f"Email: {user_with_id_1['email']}")
else:
    print("No user found with the username 'example_user' or email not available.")
if user_with_id_1:
    print(f"User with ID 1: {user_with_id_1}")
else:
    print("No user found with ID 1.")

