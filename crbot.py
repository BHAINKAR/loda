import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from flask import Flask, request

BOT_TOKEN = "7891650615:AAGouXpn6PhCz0eOrWhRLhnViTAPyE8k4No"
OWNER_ID = 5727462573  # Replace with your Telegram user ID
CHANNEL_ID = "@crunchyrollacc"

bot = telebot.TeleBot(BOT_TOKEN)
accounts_stock = []
cooldowns = {}

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

# Welcome new users
@bot.message_handler(commands=['start'])
def welcome_user(message):
        bot.send_message(
        message.chat.id,
        "🎉 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗧𝗛𝗘 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥 𝗕𝗢𝗧!\n\n"
        "Tʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴄʜᴏᴏsɪɴɢ ᴏᴜʀ sᴇʀᴠɪᴄᴇ. Wᴇ ᴀʀᴇ ᴅᴇᴅɪᴄᴀᴛᴇᴅ ᴛᴏ ᴘʀᴏᴠɪᴅɪɴɢ ғᴀsᴛ, sᴇᴄᴜʀᴇ, ᴀɴᴅ ʀᴇʟɪᴀʙʟᴇ ᴀᴄᴄᴏᴜɴᴛ ɢᴇɴᴇʀᴀᴛɪᴏɴ.\n\n"
        "📦 Yᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴀᴄᴄᴏᴜɴᴛ sᴛᴏᴄᴋ ᴀᴛ ᴀɴʏ ᴛɪᴍᴇ ᴜsɪɴɢ ᴛʜᴇ /checkstock ᴄᴏᴍᴍᴀɴᴅ.\n\n"
        "📌 Sᴛᴀʏ ᴛᴜɴᴇᴅ ғᴏʀ ᴜᴘᴅᴀᴛᴇs ᴀɴᴅ ғᴇᴇʟ ғʀᴇᴇ ᴛᴏ ʀᴇᴀᴄʜ ᴏᴜᴛ ɪғ ʏᴏᴜ ɴᴇᴇᴅ ᴀɴʏ ᴀssɪsᴛᴀɴᴄᴇ. Wᴇ'ʀᴇ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ!\nDᴍ @bhainkar\nBᴏᴛ ʙʏ @bhainkar"
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
            bot.reply_to(message, "❌ Usᴀɢᴇ:\n/add email:password\nemail:password")
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
            bot.reply_to(message, "❌ Usᴀɢᴇ:\n/remove email:password\nemail:password")
    else:
        bot.reply_to(message, "❌ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴅᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

# Check account stock
@bot.message_handler(commands=['checkstock'])
def check_stock(message):
    if len(accounts_stock) > 0:
        bot.reply_to(message, f"📦 𝗖𝗨𝗥𝗥𝗘𝗡𝗧 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗦𝗧𝗢𝗖𝗞: {len(accounts_stock)}.")
    else:
        bot.reply_to(message, "❌ Cᴜʀʀᴇɴᴛʟʏ, ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴄᴏᴜɴᴛs ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴛʜᴇ sᴛᴏᴄᴋ.\nPʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ!")

# Generate account (Send message to channel)
@bot.message_handler(commands=['genmenu'])
def generate_account(message):
    # Simply notify the user that the request is being sent to the channel
    bot.reply_to(message, "✅ Fʀᴇᴇ Cʀᴜɴᴄʜʏʀᴏʟʟ Aᴄᴄ Gᴇɴᴇʀᴀᴛᴏʀ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ {CHANNEL_ID}!")

    if len(accounts_stock) > 0:
        # Prepare the interactive button for account generation
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("✅ 𝗚𝗘𝗡 𝗔𝗖𝗖", callback_data="generate_account")
        markup.add(button)

        # Prepare and send the message to the channel
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
        # Notify if there are no accounts available for generation
        bot.reply_to(message, "❌ Cᴜʀʀᴇɴᴛʟʏ, ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴄᴏᴜɴᴛs ᴀᴠᴀɪʟᴀʙʟʀ ɪɴ ᴛʜᴇ sᴛᴏᴄᴋ.\nPʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ!")


# Handle the callback when the user clicks "GEN ACC"
@bot.callback_query_handler(func=lambda call: call.data == 'generate_account')
def send_account(call):
    user_id = call.from_user.id

    try:
        # Check if accounts are available for generation
        if len(accounts_stock) == 0:
            bot.answer_callback_query(
                call.id,
                "⚠️ Cᴜʀʀᴇɴᴛʟʏ, ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴄᴏᴜɴᴛs ᴀᴠᴀɪʟᴀʙʟʀ ɪɴ ᴛʜᴇ sᴛᴏᴄᴋ.\nPʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ!",
                show_alert=True
            )
            return

        # Check cooldown for the user
        if user_id in cooldowns and time.time() - cooldowns[user_id] < 6 * 60 * 60:
            remaining = 6 * 60 * 60 - (time.time() - cooldowns[user_id])
            bot.answer_callback_query(
                call.id,
                f"⏳ Yᴏᴜ ᴍᴜsᴛ ᴡᴀɪᴛ {int(remaining / 3600)} ʜᴏᴜʀs ᴀɴᴅ {int((remaining % 3600) / 60)} ᴍɪɴᴜᴛᴇs ʙᴇғᴏʀᴇ ɢᴇɴᴇʀᴀᴛɪɴɢ ᴀɴᴏᴛʜᴇʀ ᴀᴄᴄᴏᴜɴᴛ.",
                show_alert=True
            )
            return

        # Try sending a private message to check if the user has started the bot
        try:
            bot.send_message(user_id, "Sᴇɴᴅɪɴɢ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ. Pʟᴇᴀsᴇ ᴡᴀɪᴛ....")
        except telebot.apihelper.ApiTelegramException as e:
            # Handle the case where the bot can't send a message (User hasn't started the bot)
            if "bot can't initiate conversation with a user" in str(e) or "bot was blocked by the user" in str(e):
                bot.answer_callback_query(
                    call.id,
                    f"❌ Yᴏᴜ ᴍᴜsᴛ ғɪʀsᴛ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ɪɴ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ᴛᴏ ᴜsᴇ ᴛʜᴇ ɢᴇɴᴇʀᴀᴛᴏʀ.\n"
                    f"Sᴇɴᴅ /start ᴀᴛ https://t.me/crunchyrollaccbot",
                    show_alert=True
                )
                return

        # If the bot is not blocked and user has started, proceed with account generation
        account = accounts_stock.pop(0)  # Pop one account from the stock
        cooldowns[user_id] = time.time()  # Set the cooldown for this user

        # Send the generated account details to the user
        bot.send_message(
            user_id,
            f"✨ Yᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ:\n\n"
            f"📧 <b>Aᴄᴄᴏᴜɴᴛ</b>: <code>{account}</code>\n\n"
            f"Tʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴜsɪɴɢ ᴏᴜʀ sᴇʀᴠɪᴄᴇ!\n\n"
            f"🔑 Eɴᴊᴏʏ ʏᴏᴜʀ ᴀᴄᴄᴇss ᴀɴᴅ ғᴇᴇʟ ғʀᴇᴇ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀɴᴏᴛʜᴇʀ ᴏɴᴇ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴏʟᴅᴏᴡɴ ᴘᴇʀɪᴏᴅ.\n"
            f"𝑵𝑶𝑻𝑬: Iᴛs ғʀᴇᴇ ᴀᴄᴄ ɢᴇɴᴇʀᴀᴛᴏʀ. Sᴏ ɴᴏ ɢᴜᴀʀᴀɴᴛᴇᴇ ᴏғ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴏᴜɴᴛ",
            parse_mode='HTML'
        )

        # Notify the callback that the account is sent to the user's DMs
        bot.answer_callback_query(call.id, "✅ Aᴄᴄᴏᴜɴᴛ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ʏᴏᴜʀ DMs. Pʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ DMs.")

    except Exception as e:
        # Log unexpected errors and send them to the terminal
        print(f"⚠️ Error during account generation: {e}")
        bot.answer_callback_query(call.id, "❌ An error occurred while processing your request. Please try again later.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://loda-6opp.onrender.com/" + bot.token)  # Replace with your server URL
    app.run(host="0.0.0.0", port=5000)
