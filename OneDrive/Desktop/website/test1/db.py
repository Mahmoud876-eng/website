from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import variable
print(variable.password)
uri = variable.password
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["user_database"]
medecine_collection= db["medicines"]
id_collection = db["id"]
patient_collection = db["patient"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
id_with_id = id_collection.find({ "dr_id": id })
# Extract all numbers into a list
numbers = [str(doc['number']).strip() for doc in id_with_id]
print(numbers)
# Now find all patients whose phone is in the list of numbers
patient_with_number = patient_collection.find({ "phone": { "$in": numbers } })
#patients = [c['name'] for c in patient_with_number]
#print(patients)
patient=list(patient_with_number)
print(patient)
#for p in patient_collection.find():
 #   print("Patient phone:", p.get("name"))


