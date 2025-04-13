from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import sys

numb = sys.argv[1]
id = sys.argv[2]

TOKEN = '7780647564:AAFkPaAkOSno26OpeDPsJwF7ytz8xuzCYOg'

# Conversation states
PHOTO, TIME, NAME, NOTES = range(4)

# Temporary storage for user data
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text(numb)
    await update.message.reply_text("id")

async def add_a_med_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the /add_a_med conversation."""
    await update.message.reply_text("What is the name of the medicine.")
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

async def add_a_med_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the time period."""
    time_period = update.message.text
    context.user_data['time_period'] = time_period
    
    

    # Ask for the medicine name
    await update.message.reply_text("Do you have any notes about this medicine?")
    return NOTES

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
    context.user_data['notes'] = notes

    # Save the data (you can replace this with saving to a database or file)
    medicine_name = context.user_data['medicine_name']
    photo_file_id = context.user_data['photo_file_id']
    time_period = context.user_data['time_period']
    
    
    notes = context.user_data['notes']
    # Log the data for now
    
    

    # End the conversation
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation."""
    await update.message.reply_text("Medicine addition canceled.")
    return ConversationHandler.END
    


def main():
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))

    # triger of the functions
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_a_med", add_a_med_start)],
        states={
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