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
num=''
TOKEN =variable.TOKEN

# Conversation states
PHOTO, TIME, NAME, NOTES, PATIENT, REST = range(6)
EMAIL, PASSWORD = range(6,8)
PATIENTS, DOCTOR, NUMBER , TIMES, DATE, NOTE = range(8,14)

# Temporary storage for user data
user_data = {}
ren_data={}

#start
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
            await update.message.reply_text("You have a rendezvous with " + us["doctor"])
            await update.message.reply_text("Date: " + us["date"])
            await update.message.reply_text("Time: " + us["time"])
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

#add_a_med
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

    await update.message.reply_text("medecine succefully added.")
    
    # End the conversation
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation."""
    await update.message.reply_text("your command had been cancelled.")
    return ConversationHandler.END

#rendez vous
async def add_a_ren_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the /add_a_med conversation."""
    global id
    if not id:
        await update.message.reply_text("please do /start first")   
        return ConversationHandler.END 
    await update.message.reply_text("What is the name of the patient.")
    
    return PATIENTS

async def add_ren_patient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the patient name."""
    patient_name = update.message.text
    context.user_data['patient_ren'] = patient_name
    patient = patient_collection.find_one({"name": patient_name})
    if not patient:
        await update.message.reply_text("Patient not found. Please enter a valid patient name.")
        return PATIENTS
    await update.message.reply_text("please write the number we call u on.")
    return NUMBER   

async def add_ren_number(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    number = update.message.text
    context.user_data['number_ren'] = number
    name = context.user_data['patient_ren']
    patient_with_number = patient_collection.find_one({"name": name})
    global num
    
    if not number.isdigit() and not patient_with_number['phone']==number :
        await update.message.reply_text("Please enter a valid number of the doctor.")
        return NUMBER
    num=number
    # Ask for any additional notes
    await update.message.reply_text("please send the name of the doctor.")
    return DOCTOR

async def add_ren_doctor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the patient name."""
    name = update.message.text
    context.user_data['doctor_ren'] = name
    patient = doctor_collection.find_one({"username": name})
    if not patient:
        await update.message.reply_text("doctor not found. Please enter a valid patient name.")
        return DOCTOR
    await update.message.reply_text("please send the date of the rendez vous in the form of yyyy-mm-dd.")
    return DATE    

async def add_ren_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the patient name."""
    times = update.message.text
    print("nice")
    context.user_data['date_ren'] = times
    if not times.isdigit:
        await update.message.reply_text("error date")
        return DATE
    if "-" not in times:
        await update.message.reply_text(" Please include dashes like YYYY-MM-DD")
        return DATE
    await update.message.reply_text("please send me when u will come")
    return TIMES 

async def add_ren_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the patient name."""
    date = update.message.text
    
    if not date:
        await update.message.reply_text("error date")
        return DATE
    if ":" not in date or len(date.split(":")) != 2:
        await update.message.reply_text("Please include time in the format HH:MM.")
        return DATE
    await update.message.reply_text("please send me notes.")
    context.user_data['time_ren'] = date
    return NOTE

async def add_ren_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the notes and save all data."""
    notes = update.message.text
    print(notes)
    global id
    
    number=context.user_data['number_ren']
    patient_name=context.user_data['patient_ren']
    doctor_name=context.user_data['doctor_ren']
    date=context.user_data['date_ren']

    # Check if 'time_ren' exists
    if 'time_ren' not in context.user_data:
        await update.message.reply_text("Error: Please provide the time first.")
        return NOTE
    
    time=context.user_data['time_ren']

    # Save the data (you can replace this with saving to a database or file)
    doctor_with_id=doctor_collection.find_one({"username": doctor_name})
    
  
    # Log the data for now
    rendezvous_data = {
            "id": doctor_with_id['_id'],
            "user_id": id,
            "name": patient_name,
            "number": number,
            "doctor": doctor_name,
            "date": date,
            "time": time,
            "notes": notes
    }
    
    rendezvous_collection.insert_one(rendezvous_data)
    await update.message.reply_text("rendezvous added.")
    # End the conversation
    return ConversationHandler.END

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation."""
    global id
    id=''
    await update.message.reply_text("the account had closed.")
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
    application.add_handler(CommandHandler("clear", clear))
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

    conv_handler_ren = ConversationHandler(
        entry_points=[CommandHandler("add_a_rendezvous", add_a_ren_start)],
        states={
            NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_ren_number)],
            PATIENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_ren_patient)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_ren_date)],
            TIMES: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_ren_time)],
            DOCTOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_ren_doctor)],
            NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_ren_notes)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler_ren)

    print("Bot is running... Send it a message!")
    application.run_polling()

if __name__ == '__main__':
    main()
