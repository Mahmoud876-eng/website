from pymongo import MongoClient , DESCENDING
from pymongo.server_api import ServerApi
import variable
uri = variable.password 
# Connect to MongoDB server
client = MongoClient(uri, server_api=ServerApi('1'))

# Create a database
db = client["user_database"]

# Create a collection
users_collection = db["users"]
medecines_collection = db["medicines"]
'''''''''
# Example user data

# Insert user data into the collection
# Insert user data into the collection with auto-generated ObjectId

# Retrieve and print all inserted data
#    print(f"Inserted User: {user}")
# Check if the email exists in the database
# Insert example user data
user_data = {"name": "John Doe", "email": "johndoe@example.com"}
inserted_user = users_collection.insert_one(user_data)

# Print the ID of the inserted user
print(f"Inserted User ID: {inserted_user.inserted_id}")


# Update the user data in the collection, including changing the email and deleting the name
updated_data = {"$set": {"email": "great@mail.com"}, "$unset": {"name": ""}}

# Check if the email exists in the database
existing_user = users_collection.find_one({"email": "nice@mail.com"})

if existing_user:
   print("Old Data:", existing_user)
   # Update the user data in the collection
   update_result = users_collection.update_one({"email": "nice@mail.com"}, updated_data)
   if update_result.modified_count > 0:
      updated_user = users_collection.find_one({"email": "nice@mail.com"})
      print("New Data:", updated_user)
      print("User data updated successfully.")
      # Return the updated user's name
      if "name" in updated_user:
         print("Updated User Name:", updated_user["name"])
      else:
         print("Name field has been deleted.")
   else:
      print("User data was not updated.")
else:
   print("No matching user found with the specified email.")
   # print(f"User with ID 1: {user_with_id_1}")
#else:
    #print("No user found with ID 1.")
   # Retrieve and print the document with both ID and username
   user_with_id_and_name = users_collection.find_one({"_id": inserted_user.inserted_id, "name": "John Doe"})
  # if user_with_id_and_name:
   #   print("Retrieved Document:", user_with_id_and_name)
 #  else:
  #    print("No document found with the specified ID and username.")
      # Delete a document from the collection
  # delete_result = users_collection.delete_one({"email": "mahmoudmalek2004@gmail.com"})
   delete_result=0
   '''''
   # Retrieve the last document added to the medecines collection

# Retrieve the last document added to the medecines collection
last_doc = medecines_collection.find_one(sort=[("_id", DESCENDING)])
if last_doc:
   print("Last Document Added:", last_doc)
else:
   print("No documents found in the medecines collection.")
