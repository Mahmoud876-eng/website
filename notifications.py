import asyncio
from telegram import Bot , Update
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import variable

uri = variable.password
print(uri)
# Connect to MongoDB server
client = MongoClient(uri, server_api=ServerApi('1'))

# Create a database
db = client["user_database"]

# call collections
medecine_collection= db["medicines"]


TOKEN = variable.TOKEN
CHAT_ID = variable.CHAT_ID 
bot = Bot(token=TOKEN)

async def send_message_group():
    medecine_with_morning=medecine_collection.find({"patient": "mahmoud", "time": "morning"})
    medecine_with_afternon=medecine_collection.find({"patient": "mahmoud", "time": "Afternoon"})
    medecine_with_night=medecine_collection.find({"patient": "mahmoud", "time": "evening"})
    
    
    await bot.send_message(chat_id=CHAT_ID, text="good morning mahmomoud it s time to take your medecines:")
    await asyncio.sleep(3)

    morning=list(medecine_with_morning)
    afternon=list(medecine_with_afternon)
    night=list(medecine_with_night)
    print (morning)
    for c in morning:
        t="please take your medecien "+c["med_name"]+" don't forget "+c["notes"]
        await bot.send_message(chat_id=CHAT_ID, text=t)
        await asyncio.sleep(3)  
    await asyncio.sleep(1)
    await bot.send_message(chat_id=CHAT_ID, text="good afternnon mahmomoud it s time to take your medecines:")
    for d in afternon:
        t="please take your medecien "+d["med_name"]+" don't forget "+d["notes"]
        await bot.send_message(chat_id=CHAT_ID, text=t)
        await asyncio.sleep(3)  
    await asyncio.sleep(1)
    if medecine_with_night:
        await bot.send_message(chat_id=CHAT_ID, text="good night mahmomoud it s time to take your medecines:")
    for z in night:
        t="please take your medecien "+z["med_name"]+" don't forget "+z["notes"]
        await bot.send_message(chat_id=CHAT_ID, text=t)
        await asyncio.sleep(3)  

# === MAIN LOOP ===
async def main_loop():
    while True:
        await send_message_group()
        await asyncio.sleep(68400)  

# === RUN ===
if __name__ == '__main__':
    asyncio.run(main_loop())
