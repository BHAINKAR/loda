import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from telebot.apihelper import ApiTelegramException
from telebot import types
from flask import Flask, request

BOT_TOKEN = "7891650615:AAGouXpn6PhCz0eOrWhRLhnViTAPyE8k4No"
OWNER_ID = 5727462573  # Replace with your Telegram user ID
CHANNEL_ID = "@crunchyrollacc"

bot = telebot.TeleBot(BOT_TOKEN)
accounts_stock = []
cooldowns = {}
user_database = set()

app = Flask(__name__)

@app.route('/' + bot.token, methods=['POST'])
def get_message():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route("/", methods=['GET'])
def index():
    return "Bot is running!"
    
# Utility: Validate email:password format
def validate_accounts(input_text):
    lines = input_text.strip().split("\n")
    valid_accounts = [line.strip() for line in lines if ":" in line and len(line.split(":")) == 2]
    return valid_accounts

# Utility: Validate email:password format
def validate_accounts(input_text):
    lines = input_text.strip().split("\n")
    valid_accounts = [line.strip() for line in lines if ":" in line and len(line.split(":")) == 2]
    return valid_accounts

@bot.message_handler(commands=['start'])
def welcome_user(message):
    user_id = message.chat.id

    # Save user ID for broadcasting
    user_database.add(user_id)

    bot.send_message(
        user_id,
        "🎉 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗧𝗛𝗘 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥 𝗕𝗢𝗧!\n\n"
        "Tʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴄʜᴏᴏsɪɴɢ ᴏᴜʀ sᴇʀᴠɪᴄᴇ. Fᴀsᴛ, sᴇᴄᴜʀᴇ, ᴀɴᴅ ʀᴇʟɪᴀʙʟᴇ ᴀᴄᴄᴏᴜɴᴛ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴀᴛ ʏᴏᴜʀ ғɪɴɢᴇʀᴛɪᴘs.\n\n"
        "📦 Cʜᴇᴄᴋ sᴛᴏᴄᴋ ᴜsɪɴɢ /checkstock.\n\n"
        "Bᴏᴛ ʙʏ @bhainkar"
    )


# Add accounts to stock (Owner only, supports mass add)
@bot.message_handler(commands=['add'])
def add_accounts(message):
    if message.from_user.id == OWNER_ID:
        try:
            accounts = validate_accounts(message.text.split("\n", 1)[1])
            if accounts:
                accounts_stock.extend(accounts)
                bot.reply_to(
                    message, f"✅ Sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ {len(accounts)} Aᴄᴄᴏᴜɴᴛs ᴛᴏ ᴛʜᴇ sᴛᴏᴄᴋ."
                )
            else:
                bot.reply_to(message, "❌ Nᴏ ᴠᴀʟɪᴅ ᴀᴄᴄᴏᴜɴᴛs ғᴏᴜɴᴅ ᴛᴏ ᴀᴅᴅ. Usᴇ `email:password` ғᴏғᴍᴀᴛ.")
        except IndexError:
            bot.reply_to(message, "❌ Usᴀɢᴇ:\n/add\nemail:password\nemail:password")
    else:
        bot.reply_to(message, "❌ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

# Remove accounts from stock (Owner only, supports mass remove)
@bot.message_handler(commands=['remove'])
def remove_accounts(message):
    if message.from_user.id == OWNER_ID:
        try:
            accounts_to_remove = validate_accounts(message.text.split("\n", 1)[1])
            if accounts_to_remove:
                removed_count = 0
                for account in accounts_to_remove:
                    if account in accounts_stock:
                        accounts_stock.remove(account)
                        removed_count += 1
                bot.reply_to(
                    message, f"✅ Sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ {removed_count} Aᴄᴄᴏᴜɴᴛs ғʀᴏᴍ ᴛʜᴇ sᴛᴏᴄᴋ."
                )
            else:
                bot.reply_to(message, "❌ Nᴏ ᴠᴀʟɪᴅ ᴀᴄᴄᴏᴜɴᴛs ғᴏᴜɴᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ.")
        except IndexError:
            bot.reply_to(message, "❌ Usᴀɢᴇ:\n/remove\nemail:password\nemail:password")
    else:
        bot.reply_to(message, "❌ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴅᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

# Check account stock
@bot.message_handler(commands=['checkstock'])
def check_stock(message):
    if len(accounts_stock) > 0:
        bot.reply_to(message, f"📦 𝗖𝗨𝗥𝗥𝗘𝗡𝗧 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗦𝗧𝗢𝗖𝗞: {len(accounts_stock)}.")
    else:
        bot.reply_to(message, "❌ Cᴜʀʀᴇɴᴛʟʏ, ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴄᴏᴜɴᴛs ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴛʜᴇ sᴛᴏᴄᴋ.\nPʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ!")

@bot.message_handler(commands=['genmenu'])
def generate_account(message):
    if message.from_user.id == OWNER_ID:
        bot.reply_to(message, "✅ Fʀᴇᴇ Cʀᴜɴᴄʜʏʀᴏʟʟ Aᴄᴄ Gᴇɴᴇʀᴀᴛᴏʀ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ @crunchyrollacc !")

        if len(accounts_stock) > 0:
            markup = InlineKeyboardMarkup()
            button = InlineKeyboardButton("✅ 𝗚𝗘𝗡 𝗔𝗖𝗖", callback_data="generate_account")
            markup.add(button)

            bot.send_message(
                CHANNEL_ID,
                "🎉 <b>𝗙𝗥𝗘𝗘 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥</b>\n\n"
                "🔹 Rᴇᴀᴅʏ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛs? Cʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ǫᴜɪᴄᴋʟʏ ɢᴇᴛ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴅᴇᴛᴀɪʟs.\n\n"
                "⚡ Fᴀsᴛ, Sᴇᴄᴜʀᴇ, ᴀɴᴅ Rᴇʟɪᴀʙʟᴇ. Yᴏᴜʀ ᴀᴄᴄᴇss ɪs ᴊᴜsᴛ ᴏɴᴇ ᴄʟɪᴄᴋ ᴀᴡᴀʏ!\n\n"
                "<b>💡 𝗛𝗢𝗪 𝗧𝗢 𝗦𝗧𝗔𝗥𝗧 𝗧𝗛𝗘 𝗕𝗢𝗧?:</b>\n"
                "<i>➤ <b>Sᴛᴇᴘ 1</b>: Oᴘᴇɴ <a href='https://t.me/crunchyrollaccbot'>@crunchyrollaccbot</a> ᴀɴᴅ ᴄʟɪᴄᴋ <u>/start</u>.</i>\n"
                "<i>➤ <b>Sᴛᴇᴘ 2</b>: Wᴀɪᴛ ғᴏʀ ᴀ ᴄᴏɴғɪʀᴍᴀᴛɪᴏɴ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴛʜᴇɴ ʀᴇᴛᴜʀɴ ʜᴇʀᴇ ᴛᴏ ᴄʟɪᴄᴋ ᴛʜᴇ <b>𝗚𝗘𝗡 𝗔𝗖𝗖</b> ʙᴜᴛᴛᴏɴ.</i>\n\n"
                "Yᴏᴜ ᴍᴜsᴛ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ʙᴇғᴏʀᴇ ᴜsɪɴɢ ᴛʜᴇ ɢᴇɴᴇʀᴀᴛᴏʀ.",
                reply_markup=markup,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
        else:
            bot.reply_to(message, "❌ Nᴏ ᴀᴄᴄᴏᴜɴᴛs ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴛʜᴇ sᴛᴏᴄᴋ. Tʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ!")
    else:
        bot.reply_to(message, "❌ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

# Handle "GEN ACC" Button Click
@bot.callback_query_handler(func=lambda call: call.data == 'generate_account')
def send_account(call):
    user_id = call.from_user.id

    if len(accounts_stock) == 0:
        bot.answer_callback_query(call.id, "⚠️ Nᴏ ᴀᴄᴄᴏᴜɴᴛs ᴀᴠᴀɪʟᴀʙʟᴇ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ!", show_alert=True)
        return

    # Check cooldown (6 hours = 21600 seconds)
    if user_id in cooldowns and time.time() - cooldowns[user_id] < 21600:
        remaining = 21600 - (time.time() - cooldowns[user_id])
        bot.answer_callback_query(
            call.id,
            f"⏳ Wᴀɪᴛ {int(remaining / 3600)} ʜᴏᴜʀs {int((remaining % 3600) / 60)} ᴍɪɴᴜᴛᴇs ʙᴇғᴏʀᴇ ɢᴇɴᴇʀᴀᴛɪɴɢ ᴀɴᴏᴛʜᴇʀ ᴀᴄᴄᴏᴜɴᴛ.",
            show_alert=True
        )
        return

    # First, send a waiting message
    try:
        bot.send_message(user_id, "Sᴇɴᴅɪɴɢ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ. Pʟᴇᴀsᴇ ᴡᴀɪᴛ....")

        # Retrieve and send account
        account = accounts_stock.pop(0)
        cooldowns[user_id] = time.time()

        first_name = call.from_user.first_name
        first_name_url = f'<a href="tg://user?id={user_id}">{first_name}</a>'

        bot.send_message(
            user_id,
            f"<b>Cʀᴜɴᴄʜʏʀᴏʟʟ ᥫ᭡ Pʀᴇᴍɪᴜᴍ</b>\n\n"
            f"<b>Eᴍᴀɪʟ 📧</b>: <code>{account.split(':')[0]}</code>\n"
            f"<b>Pᴀssᴡᴏʀᴅ 🔑</b>: <code>{account.split(':')[1]}</code>\n\n"
            f"Cʜᴇᴄᴋᴇᴅ ʙʏ {first_name_url}\n"
            f"Bᴏᴛ ʙʏ @bhainkar",
            parse_mode='HTML'
        )
        time.sleep(3)

        bot.answer_callback_query(call.id, "✅ Aᴄᴄᴏᴜɴᴛ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ʏᴏᴜʀ DMs!")
    
    except telebot.apihelper.ApiTelegramException as e:
        if "bot was blocked by the user" in str(e):
            bot.answer_callback_query(call.id,"❌ 𝗕𝗢𝗧 𝗜𝗦 𝗕𝗟𝗢𝗖𝗞𝗘𝗗 𝗕𝗬 𝗬𝗢𝗨!\n\n"
            "🔓 Pʟᴇᴀsᴇ ᴜɴʙʟᴏᴄᴋ @crunchyrollaccbot ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀɴ ᴀᴄᴄᴏᴜɴᴛ.", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "⚠️ Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇ.", show_alert=True)
            
def safe_edit_message(bot, chat_id, message_id, new_text, reply_markup=None, parse_mode="HTML"):
    """
    Safely edit a message without causing a 'message is not modified' error, with parse_mode support.
    
    Args:
        bot (TeleBot): The bot instance.
        chat_id (int): The chat ID of the message.
        message_id (int): The message ID of the message to edit.
        new_text (str): The new text content for the message.
        reply_markup (InlineKeyboardMarkup, optional): The reply markup for the message.
        parse_mode (str): Parse mode for the message content (e.g., "HTML", "Markdown").
        
    Returns:
        None
    """
    try:
        # Attempt to edit the message
        bot.edit_message_text(
            text=new_text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )
    except ApiTelegramException as e:
        # Check if the error is "message is not modified"
        if "message is not modified" in str(e):
            print(f"Mᴇssᴀɢᴇ ᴄᴏɴᴛᴇɴᴛ ʜᴀs ɴᴏᴛ ᴄʜᴀɴɢᴇᴅ, sᴋɪᴘᴘɪɴɢ ᴇᴅɪᴛ.")
        else:
            # If it's a different error, re-raise it
            raise

# Button cooldown duration (6 hours)
BUTTON_COOLDOWN = 6 * 60 * 60  # 6 hours in seconds

# Dictionary to store time when user clicked the button
cooldowns = {}

@bot.message_handler(commands=['gen'])
def generate_account_private(message):
    user_id = message.from_user.id

    # Check if user is in cooldown
    if user_id in cooldowns and time.time() - cooldowns[user_id] < BUTTON_COOLDOWN:
        remaining = BUTTON_COOLDOWN - (time.time() - cooldowns[user_id])
        bot.send_message(
            user_id,
            f"⏳ Yᴏᴜ ᴀʀᴇ ɪɴ ᴄᴏᴏʟᴅᴏᴡɴ! Pʟᴇᴀsᴇ ᴡᴀɪᴛ {int(remaining / 3600)} ʜᴏᴜʀs {int((remaining % 3600) / 60)} ᴍɪɴᴜᴛᴇs ʙᴇғᴏʀᴇ ɢᴇɴᴇʀᴀᴛɪɴɢ ᴀɴᴏᴛʜᴇʀ ᴀᴄᴄᴏᴜɴᴛ."
        )
        return

    # Check if accounts are available
    if len(accounts_stock) == 0:
        bot.send_message(user_id, "❌ Nᴏ ᴀᴄᴄᴏᴜɴᴛs ᴀᴠᴀɪʟᴀʙʟᴇ ᴀᴛ ᴛʜᴇ ᴍᴏᴍᴇɴᴛ.")
        return

    # Send message asking to finalize or cancel the order
    markup = types.InlineKeyboardMarkup()
    finalize_button = types.InlineKeyboardButton("✅ 𝗚𝗘𝗡 𝗔𝗖𝗖", callback_data="finalize_gen")
    cancel_button = types.InlineKeyboardButton("❌ 𝗖𝗔𝗡𝗖𝗘𝗟", callback_data="cancel_gen")
    markup.add(finalize_button, cancel_button)

    bot.send_message(
        user_id,
        "🤔 Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴛʜᴇ \n𝗙𝗥𝗘𝗘 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟 𝗔𝗖𝗖𝗢𝗨𝗡𝗧?",
        reply_markup=markup
    )

# Handle the "Finalize" and "Cancel" button click
@bot.callback_query_handler(func=lambda call: call.data in ['finalize_gen', 'cancel_gen'])
def handle_finalization(call):
    user_id = call.from_user.id
    message_id = call.message.message_id

    # Safely edit the message to show the process is happening
    safe_edit_message(bot, call.message.chat.id, message_id, "Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ...")

    if call.data == 'finalize_gen':
        # Check if accounts are available
        if len(accounts_stock) == 0:
            bot.answer_callback_query(call.id, "❌ Nᴏ ᴀᴄᴄᴏᴜɴᴛs ᴀᴠᴀɪʟᴀʙʟᴇ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.", show_alert=True)
            return

        # Proceed with account generation if user finalized
        account = accounts_stock.pop(0)
        cooldowns[user_id] = time.time()  # Set cooldown for 6 hours
        first_name = call.from_user.first_name
        first_name_url2 = f'<a href="tg://user?id={user_id}">{first_name}</a>'
        
        # Send account details
        bot.send_message(
            user_id,
            f"<b>Cʀᴜɴᴄʜʏʀᴏʟʟ ᥫ᭡ Pʀᴇᴍɪᴜᴍ</b>\n\n"
            f"<b>Eᴍᴀɪʟ 📧</b>: <code>{account.split(':')[0]}</code>\n"
            f"<b>Pᴀssᴡᴏʀᴅ 🔑</b>: <code>{account.split(':')[1]}</code>\n\n"
            f"Cʜᴇᴄᴋᴇᴅ ʙʏ {first_name_url2}\n"
            f"Bᴏᴛ ʙʏ @Bhainkar",
            parse_mode='HTML'
        )
        time.sleep(3)
        safe_edit_message(bot, call.message.chat.id, message_id, "Aᴄᴄᴏᴜɴᴛ ʜᴀs ʙᴇᴇɴ ɢᴇɴᴇʀᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")

    elif call.data == 'cancel_gen':
        # Safely edit the message to show cancellation
        safe_edit_message(bot, call.message.chat.id, message_id, "Aᴄᴄᴏᴜɴᴛ ɢᴇɴᴇʀᴀᴛɪᴏɴ ʜᴀs ʙᴇᴇɴ ᴄᴀɴᴄᴇʟᴇᴅ.")

        first_name = call.from_user.first_name
        first_name_url3 = f'<a href="tg://user?id={user_id}">{first_name}</a>'
        bot.send_message(user_id, f"🛑 Gᴇɴᴇʀᴀᴛɪᴏɴ ᴄᴀɴᴄᴇʟᴇᴅ Bʏ {first_name_url3}", parse_mode='HTML')

owner_draft = {}
OWNER_ID2 = "5727462573"  # Replace with your actual Telegram ID

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    user_id = str(message.from_user.id)

    if user_id != OWNER_ID2:
        bot.send_message(message.chat.id, "⛔ Unauthorized! Only the owner can broadcast messages.")
        return

    broadcast_message = message.text.partition(" ")[2]
    if not broadcast_message.strip():
        bot.send_message(message.chat.id, "⚠️ Please use /broadcast MESSAGE to create a draft.")
        return

    owner_draft[user_id] = broadcast_message
    bot.send_message(
        message.chat.id, 
        "✍️ Your broadcast draft has been saved.\n\nUse the following commands:\n"
        "👁 /preview - Preview the message\n"
        "📢 /send - Send the message to all users."
    )

@bot.message_handler(commands=['preview'])
def preview(message):
    user_id = str(message.from_user.id)

    if user_id != OWNER_ID2:
        bot.send_message(message.chat.id, "⛔ Unauthorized!")
        return

    broadcast_message = owner_draft.get(user_id)
    if not broadcast_message:
        bot.send_message(message.chat.id, "⚠️ No draft found. Use /broadcast to create a message first.")
        return

    bot.send_message(message.chat.id, f"👁 <b>Broadcast Preview:</b>\n\n{broadcast_message}", parse_mode='HTML')

@bot.message_handler(commands=['send'])
def send_broadcast(message):
    user_id = str(message.from_user.id)

    if user_id != OWNER_ID2:
        bot.send_message(message.chat.id, "⛔ Unauthorized! Only the owner can send broadcast messages.")
        return

    broadcast_message = owner_draft.get(user_id)
    if not broadcast_message:
        bot.send_message(message.chat.id, "⚠️ No draft found. Use /broadcast to create a message first.")
        return

    sent_count = 0
    failed_count = 0

    for user_id in user_database:
        try:
            bot.send_message(user_id, broadcast_message, disable_web_page_preview=True)
            sent_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Failed to send message to {user_id}: {e}")  

    bot.send_message(
        message.chat.id,
        f"✅ Broadcast sent successfully.\n"
        f"👥 Total Users: {len(user_database)}\n✅ Sent: {sent_count}\n❌ Failed: {failed_count}"
    )

    owner_draft.pop(user_id, None)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://loda-6opp.onrender.com/" + bot.token)  # Replace with your server URL
    app.run(host="0.0.0.0", port=5000)
