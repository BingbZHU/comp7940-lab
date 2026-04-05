# This program evolves the lab chatbot with cloud features
# Required modules:
# - python-telegram-bot==22.5
# - urllib3==2.6.2
# - supabase (for cloud database)

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    MessageHandler, 
    ContextTypes, 
    filters,
    CommandHandler
)
import configparser
import logging
from supabase import create_client, Client
from HogwartsGPT import ChatGPT

# Global variables
gpt = None
supabase: Client = None

# Static event data (for test)
# EVENT_DATA = [
#     {
#         "title": "Hogwarts Castle Nighttime Light Show at Universal Beijing",
#         "time": "Daily before park closing, 2026",
#         "link": "https://www.universalbeijingresort.com/en",
#         "target_houses": ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
#     },
#     {
#         "title": "Slytherin House Themed Afternoon Tea",
#         "time": "Every Saturday, April-June 2026",
#         "link": "https://www.universalbeijingresort.com/en/dining",
#         "target_houses": ["Slytherin"]
#     },
#     {
#         "title": "Gryffindor Warrior Challenge",
#         "time": "May 2026",
#         "link": "https://www.harrypotterfanclub.com/",
#         "target_houses": ["Gryffindor"]
#     }
# ]

# Logging config (same as lab)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # Load config (same as lab)
    logging.info('INIT: Loading configuration...')
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Initialize Supabase (cloud database)
    global supabase
    supabase = create_client(config['SUPABASE']['URL'], config['SUPABASE']['KEY'])
    logging.info('INIT: Cloud database connected')

    # Initialize LLM (same as lab)
    global gpt
    gpt = ChatGPT(config)
    logging.info('INIT: LLM client initialized')

    # Initialize Telegram Bot (same as lab)
    logging.info('INIT: Connecting Telegram bot...')
    app = ApplicationBuilder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()

    # Register handlers (evolved from lab)
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("choose_house", choose_house_command))
    app.add_handler(CommandHandler("match", match_command))
    app.add_handler(CommandHandler("events", events_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_callback))

    # Start bot (same as lab)
    logging.info('INIT: Initialization done! Bot started.')
    app.run_polling()

# ---------------------- Command Handlers ----------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Auto-save new user to cloud database
    supabase.table('users').upsert({'user_id': user_id}).execute()
    
    welcome_text = (
        "🧙‍♂️ Welcome to Hogwarts Guide!\n"
        "I can help you with:\n"
        "📍 Campus navigation & routes\n"
        "🎯 Send 'event' for house activities\n"
        "🏠 /choose_house to select your house\n"
        "🎮 /match to find housemates\n"
    )
    await update.message.reply_text(welcome_text)

async def choose_house_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    house_options = (
        "🏰 Please select your Hogwarts house:\n\n"
        "1. Gryffindor 🦁\n"
        "2. Hufflepuff 🦡\n"
        "3. Ravenclaw 🦅\n"
        "4. Slytherin 🐍\n\n"
        "Reply with the house name to confirm!"
    )
    await update.message.reply_text(house_options)

async def match_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Get user's house from cloud database
    user_res = supabase.table('users').select('house_name').eq('user_id', user_id).execute()
    
    if not user_res.data or not user_res.data[0]['house_name']:
        await update.message.reply_text("❌ Please select your house first with /choose_house!")
        return
    
    user_house = user_res.data[0]['house_name']
    # Get ALL house members, EXCLUDE yourself
    members_res = supabase.table('users').select('user_id').eq('house_name', user_house).execute()
    housemates = [str(m['user_id']) for m in members_res.data if m['user_id'] != user_id]
    member_count = len(housemates) + 1  # +1 for yourself

    # Build Harry Potter themed response
    match_text = f"✨ {user_house} Common Room Connection Activated!\n\n"
    match_text += f"Total wizards in {user_house}: {member_count}\n\n"
    
    if member_count == 1:
        match_text += "You're the first witch/wizard of your house here! 🧙\nInvite your friends to join and connect via Hogwarts Owl Post!"
    else:
        match_text += f"Your {user_house} housemates (Owl Post IDs):\n"
        for idx, mate_id in enumerate(housemates, 1):
            match_text += f"{idx}. `{mate_id}`\n"
        match_text += "\nShare their ID via Owl Post to chat and explore Hogwarts together!"
    
    await update.message.reply_text(match_text)

async def events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Get user's house
    user_res = supabase.table('users').select('house_name').eq('user_id', user_id).execute()
    user_house = user_res.data[0]['house_name'] if user_res.data and user_res.data[0]['house_name'] else None

    # Filter events by house
    if user_house:
        filtered_events = [e for e in EVENT_DATA if user_house in e['target_houses']]
        recommend_text = f"🎡 Recommended events for {user_house}:\n\n"
    else:
        filtered_events = EVENT_DATA
        recommend_text = "🎡 Recommended Harry Potter events:\n\n"

    # Build event list
    for event in filtered_events[:3]:
        recommend_text += f"📌 {event['title']}\n📅 Time: {event['time']}\n🔗 Details: {event['link']}\n\n"
    
    await update.message.reply_text(recommend_text)

# ---------------------- Message Handler ----------------------
async def chat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    logging.info(f"Received message from user {user_id}: {user_message}")

    # Handle house selection reply
    house_list = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
    if user_message in house_list:
        supabase.table('users').update({'house_name': user_message}).eq('user_id', user_id).execute()
        await update.message.reply_text(f"🎉 Welcome to {user_message}! Your magic journey begins!")
        # Log to cloud database
        supabase.table('chat_logs').insert({
            'user_id': user_id,
            'user_message': user_message,
            'bot_response': f"Joined {user_message}"
        }).execute()
        return


    
    if "event" in user_message.lower() or "events" in user_message:
        
        user_res = supabase.table('users').select('house_name').eq('user_id', user_id).execute()
        user_house = user_res.data[0]['house_name'] if user_res.data and user_res.data[0]['house_name'] else None

        if not user_house:
            await update.message.reply_text("Please choose your house first with /choose_house!")
            return

        # from Supabase events 
        events = supabase.table('events').select('*').or_(
            f'target_house.eq.{user_house},target_house.eq.ALL'
        ).execute().data

        if not events:
            await update.message.reply_text("No events for your house yet!")
            return

        
        text = f"🎡 Events for {user_house}:\n\n"
        for e in events[:3]:
            text += f"📌 {e['title']}\n⏰ {e['event_time']}\n🔗 {e['link']}\n\n"
        
        await update.message.reply_text(text)
        supabase.table('chat_logs').insert({
            'user_id': user_id, 'user_message': user_message, 'bot_response': text
        }).execute()
        return









    # Loading message
    loading_message = await update.message.reply_text('🔮 The magic crystal ball is thinking...')

    # Get user's house for LLM
    user_res = supabase.table('users').select('house_name').eq('user_id', user_id).execute()
    user_house = user_res.data[0]['house_name'] if user_res.data else None

    # Get LLM response
    response = gpt.submit(user_message,user_house)

    supabase.table('users').upsert({'user_id': user_id}).execute()
    
    # Log to cloud database (meets project data logging requirement)
    supabase.table('chat_logs').insert({
        'user_id': user_id,
        'user_message': user_message,
        'bot_response': response
    }).execute()

    # Send reply
    await loading_message.edit_text(response)

if __name__ == '__main__':
    main()