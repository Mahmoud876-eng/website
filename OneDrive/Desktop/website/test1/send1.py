from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from pymongo import MongoClient
from pymongo.server_api import ServerApi
#import sys
import variable

uri = variable.password
# Connect to MongoDB server
client = MongoClient(uri, server_api=ServerApi('1'))

# Create a database
db = client["user_database"]

# Create a collection
users_collection = db["users"]
medecine_collection= db["medicines"]
doctor_collection= db["doctor"]
patient_collection= db["patient"]
id_collection= db["id"]
rendezvous_collection= db["rendezvous"]


#id = sys.argv[1]
#status = sys.argv[2]
id=''
TOKEN =variable.TOKEN

# Conversation states
PHOTO, TIME, NAME, NOTES, PATIENT, REST = range(6)
EMAIL, PASSWORD = range(2)
PATIENTS, DOCTOR, NUMBER , TIMES, DATE, NOTE = range(6)

# Temporary storage for user data
user_data = {}
ren_data={}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Please type your email address.")
    chat_id = update.effective_chat.id
    print(f"Chat ID: {chat_id}")
    return EMAIL
#still haven test the user
async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global id
    print(id)
    
    if not id:
        await update.message.reply_text("please do /start first")   
        return ConversationHandler.END 
    dr_rendez_with_id=rendezvous_collection.find({"id": id})
    user_rendez_with_id=rendezvous_collection.find({"user_id":id})
    print("be happy")
    dr=list(dr_rendez_with_id)
    user=list(user_rendez_with_id)
    print(dr)
    if dr:
        print("6")
        for doc in dr:
            await update.message.reply_text("You have a rendezvous with " + doc["name"])
            await update.message.reply_text("Date: " + doc["date"])
            await update.message.reply_text("Time: " + doc["time"])
        return ConversationHandler.END
    elif user:
        for us in user:
            await update.message.reply_text("You have a rendezvous with " + user_rendez_with_id["doctor"])
            await update.message.reply_text("Date: " + user_rendez_with_id["date"])
            await update.message.reply_text("Time: " + user_rendez_with_id["time"])
        return ConversationHandler.END 
    return ConversationHandler.END    

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    context.user_data["email"] = email
    await update.message.reply_text("Thanks! Now enter your password.")
    
    user = users_collection.find_one({"email": email})
    doctor = doctor_collection.find_one({"email": email})
    
    if not user and not doctor:
        await update.message.reply_text("Email not found. Please register first.")
        return EMAIL
    return PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global id
    email = context.user_data["email"]
    password = update.message.text

    user = users_collection.find_one({"email": email})
    doctor = doctor_collection.find_one({"email": email})

    if user and user["password"] == password:
        await update.message.reply_text("You are logged in as a patient.")
        id=user["_id"]

    elif doctor and doctor["password"] == password:
        await update.message.reply_text("You are logged in as a doctor.")
        id=doctor["_id"]
        print(id)
    else:
        await update.message.reply_text("Invalid credentials. Try again.")
        return PASSWORD
    return ConversationHandler.END


async def add_a_med_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the /add_a_med conversation."""
    global id
    if not id:
        await update.message.reply_text("please do /start first")   
        return ConversationHandler.END 
    await update.message.reply_text("What is the name of the patient.")
    
    return PATIENT
async def add_a_patient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the patient name."""
    patient_name = update.message.text
    context.user_data['patient_name'] = patient_name
    patient = patient_collection.find_one({"name": patient_name})
    if not patient:
        await update.message.reply_text("Patient not found. Please enter a valid patient name.")
        return PATIENT
    await update.message.reply_text("please send le the name of the medecine.")
    return NAME



async def add_a_med_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the photo of the medicine."""
    photo = update.message.photo[-1]  # Get the highest resolution photo
    file_id = photo.file_id

    # Save the file ID in user data for later use
    context.user_data['photo_file_id'] = file_id

    # Ask for the time period
    reply_keyboard = [['Morning', 'Afternoon', 'Night']]
    await update.message.reply_text(
        "When do you take this medicine? (Choose one)",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    )
    return TIME
async def add_a_med_rest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    medicine_rest = update.message.text
    context.user_data['medecine_rest'] = medicine_rest
    if not medicine_rest.isdigit():
        await update.message.reply_text("Please enter a valid number for the medicine rest.")
        return REST

    # Ask for any additional notes
    await update.message.reply_text("please send notes of the patient.")
    return NOTES

    
async def add_a_med_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the time period."""
    time_period = update.message.text
    context.user_data['time_period'] = time_period
    
    

    # Ask for the medicine name
    await update.message.reply_text("how many medicine do u haev?")
    return REST

async def add_a_med_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the medicine name."""
    medicine_name = update.message.text
    context.user_data['medicine_name'] = medicine_name
    print(medicine_name)

    # Ask for any additional notes
    await update.message.reply_text("please send me the photo of the medicine.")
    return PHOTO

async def add_a_med_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the notes and save all data."""
    notes = update.message.text
    print(notes)
    global id
    context.user_data['notes'] = notes
    patient_name=context.user_data['patient_name']
    # Save the data (you can replace this with saving to a database or file)
    medicine_name = context.user_data['medicine_name']
    photo_file_id = context.user_data['photo_file_id']
    time_period = context.user_data['time_period']
    rest_med=context.user_data['medecine_rest']
    
    
    notes = context.user_data['notes']
    # Log the data for now
    medine_data = {
            "id": id,
            "patient": patient_name,
            "med_name": medicine_name,
            "img": photo_file_id,
            "time": time_period,
            "notes": notes,
            "rest": rest_med
    }
    medecine_collection.insert_one(medine_data)


    
    

    # End the conversation
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation."""
    await update.message.reply_text("Medicine addition canceled.")
    return ConversationHandler.END
    


def main():
    application = Application.builder().token(TOKEN).build()

    #make the prog only work only when there s start
    # Add handlers
    conv_handler_start = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler_start)
    application.add_handler(CommandHandler("view", view))
    # triger of the functions
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_a_med", add_a_med_start)],
        states={
            REST: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_a_med_rest)],
            PATIENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_a_patient)],
            PHOTO: [MessageHandler(filters.PHOTO, add_a_med_photo)],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_a_med_time)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_a_med_name)],
            NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_a_med_notes)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],

    )
    application.add_handler(conv_handler)

    print("Bot is running... Send it a message!")
    application.run_polling()

if __name__ == '__main__':
    main()
    