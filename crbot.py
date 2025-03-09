import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from telebot.apihelper import ApiTelegramException

BOT_TOKEN = "7891650615:AAGouXpn6PhCz0eOrWhRLhnViTAPyE8k4No"
OWNER_ID = 5727462573
CHANNEL_ID = "@bhainkarfeedback"
ADMINS = set()

bot = telebot.TeleBot(BOT_TOKEN)
accounts_stock = []
cooldowns = {}
user_database = set()
free_users = set()
owner_draft = {}

app = Flask(__name__)

@app.route('/' + bot.token, methods=['POST'])
def get_message():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route("/", methods=['GET'])
def index():
    return "Cʀᴜɴᴄʜʏʀᴏʟʟ ᴀᴄᴄ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ ɪs ʀᴜɴɴɪɴɢ!"
    
def validate_accounts(input_text):
    lines = input_text.strip().split("\n")
    return [line.strip() for line in lines if ":" in line and len(line.split(":", 1)) == 2]

def safe_edit_message(chat_id, message_id, new_text, reply_markup=None, parse_mode="HTML", disable_web_page_preview=True):
    try:
        bot.edit_message_text(
            text=new_text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
    except ApiTelegramException as e:
        # Ignore "message not modified" errors
        if "message is not modified" not in str(e) and "Mᴇssᴀɢᴇ ɪs ɴᴏᴛ ᴍᴏᴅɪғɪᴇᴅ" not in str(e):
            raise

@bot.message_handler(commands=['start'])
def welcome_user(message):
    user_id = message.chat.id
    user_database.add(user_id)
    free_users.add(user_id)

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ 𝗚𝗘𝗡 𝗔𝗖𝗖", callback_data="gen_acc"),
        InlineKeyboardButton("📦 𝗦𝗧𝗢𝗖𝗞", callback_data="check_stock"),
        InlineKeyboardButton("📊 𝗦𝗧𝗔𝗧𝗦", callback_data="bot_stats"),
        InlineKeyboardButton("👥 𝗨𝗦𝗘𝗥𝗟𝗜𝗦𝗧", callback_data="user_list"),
        InlineKeyboardButton("💌 𝗙𝗘𝗘𝗗𝗕𝗔𝗖𝗞", callback_data="feedback"),
        InlineKeyboardButton("🛠 𝗛𝗘𝗟𝗣", callback_data="help_menu")
    )

    first_name = message.from_user.first_name
    username = message.from_user.username
    user_id = message.from_user.id

    # Creating a clickable profile link
    if username:
        profile_link = f'<a href="https://t.me/{username}">{first_name}</a>'
    else:
        profile_link = f'<a href="tg://user?id={user_id}">{first_name}</a>'

    if message.chat.type == 'private':
        bot.send_message(
            user_id,
            f"🎉 Hᴇʏ! {profile_link} \n𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟\n𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥!! \n\n"
            "🔹 Pʀᴇᴍɪᴜᴍ Aᴄᴄᴏᴜɴᴛ Gᴇɴᴇʀᴀᴛᴏʀ\n"
            "🔹 24/7 Aᴠᴀɪʟᴀʙɪʟɪᴛʏ\n"
            "🔹 Iɴsᴛᴀɴᴛ Dᴇʟɪᴠᴇʀʏ Sʏsᴛᴇᴍ",
            reply_markup=markup,
            parse_mode="HTML",
            disable_web_page_preview=True
        )


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    handlers = {
        'gen_acc': handle_gen_acc,
        'check_stock': handle_check_stock,
        'bot_stats': show_stats,
        'user_list': show_userlist,
        'feedback': handle_feedback,
        'help_menu': handle_help,
        'confirm_gen': handle_confirmation,
        'cancel_gen': handle_confirmation,
        'back_menu': handle_back,
        '5_star': handle_star_rating,
        '4_star': handle_star_rating,
        '3_star': handle_star_rating,
        '2_star': handle_star_rating,
        '1_star': handle_star_rating
    }
    
    if call.data in handlers:
        handlers[call.data](call)

def handle_back(call):
    user_id = call.from_user.id
    first_name = call.from_user.first_name
    username = call.from_user.username

    # Create profile link
    if username:
        profile_link = f'<a href="https://t.me/{username}">{first_name}</a>'
    else:
        profile_link = f'<a href="tg://user?id={user_id}">{first_name}</a>'

    # Recreate main menu markup
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ 𝗚𝗘𝗡 𝗔𝗖𝗖", callback_data="gen_acc"),
        InlineKeyboardButton("📦 𝗦𝗧𝗢𝗖𝗞", callback_data="check_stock"),
        InlineKeyboardButton("📊 𝗦𝗧𝗔𝗧𝗦", callback_data="bot_stats"),
        InlineKeyboardButton("👥 𝗨𝗦𝗘𝗥𝗟𝗜𝗦𝗧", callback_data="user_list"),
        InlineKeyboardButton("💌 𝗙𝗘𝗘𝗗𝗕𝗔𝗖𝗞", callback_data="feedback"),
        InlineKeyboardButton("🛠 𝗛𝗘𝗟𝗣", callback_data="help_menu")
    )

    # Edit existing message instead of sending new one
    safe_edit_message(
        call.message.chat.id,
        call.message.message_id,
        f"🎉 Hᴇʏ! {profile_link} \n𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟\n𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥!! \n\n"
        "🔹 Pʀᴇᴍɪᴜᴍ Aᴄᴄᴏᴜɴᴛ Gᴇɴᴇʀᴀᴛᴏʀ\n"
        "🔹 24/7 Aᴠᴀɪʟᴀʙɪʟɪᴛʏ\n"
        "🔹 Iɴsᴛᴀɴᴛ Dᴇʟɪᴠᴇʀʏ Sʏsᴛᴇᴍ",
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    
def handle_help(call):
    user_id = call.from_user.id
    help_text = ""
    
    if user_id == OWNER_ID or user_id in ADMINS:
        help_text = (
            "🛠 <b>Aᴅᴍɪɴ Cᴍᴅs</b>\n\n"
            "𝗢𝗪𝗡𝗘𝗥:\n"
            "/addadmin [user_id] - Aᴅᴅ Aᴅᴍɪɴ\n"
            "/removeadmin [user_id] - Rᴇᴍᴏᴠᴇ Aᴅᴍɪɴ\n"
            "𝗔𝗗𝗠𝗜𝗡:\n"
            "/add [accounts] - Aᴅᴅ Aᴄᴄᴏᴜɴᴛs\n"
            "/remove [accounts] - Rᴇᴍᴏᴠᴇ Aᴄᴄᴏᴜɴᴛs\n"
            "/liststock - Sʜᴏᴡs Aᴄᴄᴏᴜɴᴛ's' Sᴛᴏᴄᴋ & Aᴄᴄᴏᴜɴᴛ's Dᴇᴛᴀɪʟs\n"
            "/broadcast - Sᴇɴᴅ ʙʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ"
        )
    else:
        help_text = (
            "📖 <b>Usᴇʀ Gᴜɪᴅᴇ</b>\n\n"
            "• Tʏᴘᴇ /start ᴀɴᴅ ᴄʟɪᴄᴋ ✅ 𝗚𝗘𝗡 𝗔𝗖𝗖  Tᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀᴄᴄᴏᴜɴᴛs\n"
            "• Yᴏᴜ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ 1 ᴀᴄᴄᴏᴜɴᴛ ᴇᴠᴇʀʏ 6 ʜᴏᴜʀs!\n"
            "• Cʜᴇᴄᴋ sᴛᴏᴄᴋ ʙᴇғᴏʀᴇ ɢᴇɴᴇʀᴀᴛɪɴɢ.\n"
            "• Sᴜʙᴍɪᴛ ғᴇᴇᴅʙᴀᴄᴋs ғᴏʀ sʜᴀʀɪɴɢ ʏᴏᴜʀ ᴇxᴘᴇʀɪᴇɴᴄᴇ."
        )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data='back_menu'))
    
    safe_edit_message(
        call.message.chat.id,
        call.message.message_id,
        help_text,
        reply_markup=markup,
        parse_mode="HTML"
    )

def handle_gen_acc(call):
    user_id = call.from_user.id
    current_time = time.time()
    
    if user_id in cooldowns:
        elapsed = current_time - cooldowns[user_id]
        if elapsed < 21600:
            remaining = 21600 - elapsed
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            bot.answer_callback_query(call.id, 
                f"⏳ Pʟᴇᴀsᴇ ᴡᴀɪᴛ {hours}ʜᴏᴜʀs {minutes}ᴍɪɴs ʙᴇғᴏʀᴇ ɢᴇɴᴇʀᴀᴛɪɴɢ ᴀɢᴀɪɴ.", 
                show_alert=True)
            return
    
    if not accounts_stock:
        bot.answer_callback_query(call.id, "⚠️ Nᴏ ᴀᴄᴄᴏᴜɴᴛs ᴀᴠᴀɪʟᴀʙʟᴇ!", show_alert=True)
        return
    
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ 𝗖𝗢𝗡𝗙𝗜𝗥𝗠", callback_data='confirm_gen'),
        InlineKeyboardButton("❌ 𝗖𝗔𝗡𝗖𝗘𝗟", callback_data='cancel_gen')
    )
    
    safe_edit_message(
        call.message.chat.id,
        call.message.message_id,
        "⚠️ Yᴏᴜ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ 1 ᴀᴄᴄᴏᴜɴᴛ ᴇᴠᴇʀʏ 6 ʜᴏᴜʀs. ✅ 𝗖𝗢𝗡𝗙𝗜𝗥𝗠?",
        reply_markup=markup
    )

def handle_confirmation(call):
    user_id = call.from_user.id
    if call.data == 'confirm_gen':
        if not accounts_stock:
            bot.answer_callback_query(call.id, "⚠️ Nᴏ ᴀᴄᴄᴏᴜɴᴛs ʟᴇғᴛ!", show_alert=True)
            return
        
        current_time = time.time()
        if user_id in cooldowns and (current_time - cooldowns[user_id] < 21600):
            bot.answer_callback_query(call.id, "⏳ Yᴏᴜ'ʀᴇ' sᴛɪʟʟ ɪɴ ᴄᴏᴏʟᴅᴏᴡɴ...!", show_alert=True)
            return
        
        account = accounts_stock.pop(0)
        email, password = account.split(':', 1)
        cooldowns[user_id] = current_time
        
        first_name = call.from_user.first_name or "User"
        first_name_url = f'<a href="tg://user?id={user_id}">{first_name}</a>'

        bot.send_message(
            user_id,
            f"<b>Cʀᴜɴᴄʜʏʀᴏʟʟ ᥫ᭡ Pʀᴇᴍɪᴜᴍ</b>\n\n"
            f"<b>Eᴍᴀɪʟ 📧</b>: <code>{email}</code>\n"
            f"<b>Pᴀssᴡᴏʀᴅ 🔑</b>: <code>{password}</code>\n\n"
            f"Cʜᴇᴄᴋᴇᴅ ʙʏ {first_name_url}\n"
            f"Bᴏᴛ ʙʏ @bhainkar",
            parse_mode='HTML'
        )
        
        safe_edit_message(
            call.message.chat.id,
            call.message.message_id,
            "✅ Aᴄᴄᴏᴜɴᴛ ʜᴀs ʙᴇᴇɴ ɢᴇɴᴇʀᴀᴛᴇᴅ!",
            reply_markup=None
        )
    else:
        safe_edit_message(
            call.message.chat.id,
            call.message.message_id,
            "❌ Gᴇɴᴇʀᴀᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.",
            reply_markup=None
        )
    bot.answer_callback_query(call.id)

def handle_check_stock(call):
    stock_text = f"📦 𝗦𝗧𝗢𝗖𝗞: {len(accounts_stock)} Aᴄᴄᴏᴜɴᴛs"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data='back_menu'))
    safe_edit_message(
        call.message.chat.id,
        call.message.message_id,
        stock_text,
        reply_markup=markup
    )

def show_stats(call):
    total_users = len(user_database)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data='back_menu'))
    
    stats_text = (
        f"📊 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦\n\n"
        f"👤 Tᴏᴛᴀʟ Usᴇʀs: {total_users}\n"
        f"👥 Aᴄᴛɪᴠᴇ Usᴇʀs: {len(free_users)}\n"
        f"📦 Sᴛᴏᴄᴋ: {len(accounts_stock)}\n"
        f"🛡 Aᴅᴍɪɴs: {len(ADMINS)}"
    )
    
    safe_edit_message(
        call.message.chat.id,
        call.message.message_id,
        stats_text,
        reply_markup=markup
    )

def show_userlist(call):
    user_list = "<b>📋 𝗨𝗦𝗘𝗥 𝗟𝗜𝗦𝗧</b>\n\n"
    for idx, user_id in enumerate(free_users, 1):
        try:
            user = bot.get_chat(user_id)
            link = f'<a href="tg://user?id={user_id}">{user.first_name}</a>'
            user_list += f"{idx}. {link} - <code>{user_id}</code>\n"
        except:
            user_list += f"{idx}. Unknown User - <code>{user_id}</code>\n"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data='back_menu'))
    
    safe_edit_message(
        call.message.chat.id,
        call.message.message_id,
        user_list,
        reply_markup=markup,
        parse_mode="HTML"
    )

def handle_feedback(call):
    try:
        # Verify real user
        if call.from_user.is_bot:
            return

        # Create rating buttons
        markup = InlineKeyboardMarkup(row_width=1)
        stars = [
            InlineKeyboardButton("🌟🌟🌟🌟🌟", callback_data="5_star"),
            InlineKeyboardButton("🌟🌟🌟🌟☆", callback_data="4_star"),
            InlineKeyboardButton("🌟🌟★☆☆", callback_data="3_star"),
            InlineKeyboardButton("★★☆☆☆", callback_data="2_star"),
            InlineKeyboardButton("★☆☆☆☆", callback_data="1_star")
        ]
        markup.add(*stars)
        markup.add(InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data='back_menu'))

        # Get user details
        user = call.from_user
        username = f"@{user.username}" if user.username else user.first_name
        
        safe_edit_message(
            call.message.chat.id,
            call.message.message_id,
            f"<b>⭐ {username}'s ʀᴀᴛɪɴɢ ᴘᴀɴᴇʟ</b>\n\n"
            "Hᴏᴡ ᴡᴏᴜʟᴅ ʏᴏᴜ ʀᴀᴛᴇ ʏᴏᴜʀ ᴇxᴘᴇʀɪᴇɴᴄᴇ?\n"
            "🌟🌟🌟🌟🌟 - Exᴄᴇʟʟᴇɴᴛ\n"
            "🌟🌟🌟🌟☆ - Vᴇʀʏ Gᴏᴏᴅ\n"
            "🌟🌟★☆☆ - Gᴏᴏᴅ\n"
            "★★☆☆☆ - Fᴀɪʀ\n"
            "★☆☆☆☆ - Pᴏᴏʀ",
            reply_markup=markup,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Feedback Error: {e}")
        bot.answer_callback_query(call.id, "❌ Rᴀᴛɪɴɢ sʏsᴛᴇᴍ ᴇʀʀᴏʀ!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.endswith("_star"))
def handle_star_rating(call):
    try:
        # Verify real user
        if call.from_user.is_bot:
            return

        # Get user details
        user = call.from_user
        stars = call.data.split("_")[0]
        username = f"@{user.username}" if user.username else user.first_name
        profile_link = f'<a href="tg://user?id={user.id}">{username}</a>'

        # 1. Edit original message first
        safe_edit_message(
            call.message.chat.id,
            call.message.message_id,
            f"⏳ Pʀᴏᴄᴇssɪɴɢ {username}'s {stars}-Sᴛᴀʀ ʀᴀᴛɪɴɢ...",
            reply_markup=None
        )

        # 2. Prepare feedback message
        feedback_msg = (
            f"📊 <b>Nᴇᴡ Fᴇᴇᴅʙᴀᴄᴋ Rᴇᴄᴇɪᴠᴇᴅ</b>\n\n"
            f"▫️ Rᴀᴛɪɴɢ: {stars} stars\n"
            f"▫️ Usᴇʀ: {profile_link}\n"
            f"▫️ Iᴅ: <code>{user.id}</code>\n"
            f"▫️ Dᴀᴛᴇ: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # 3. Send to channel
        bot.send_message(
            CHANNEL_ID,
            feedback_msg,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

        # 4. Update user message
        safe_edit_message(
            call.message.chat.id,
            call.message.message_id,
            f"✅ <b>Tʜᴀɴᴋ ʏᴏᴜ {username}!</b>\n"
            "Yᴏᴜʀ ʀᴀᴛɪɴɢ ʜᴀs ʙᴇᴇɴ ʀᴇᴄᴏʀᴅᴇᴅ\n"
            "Cʜᴇᴄᴋ ғᴇᴇᴅʙᴀᴄᴋ ᴀᴛ @bhainkarfeedback",
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as e:
        print(f"Rating Error: {e}")
        bot.answer_callback_query(call.id, "⚠️ Fᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ ʀᴀᴛɪɴɢ!", show_alert=True)

@bot.message_handler(commands=['add'])
def add_accounts(message):
    if message.from_user.id == OWNER_ID or message.from_user.id in ADMINS:
        try:
            accounts_text = message.text.split(maxsplit=1)[1]
            accounts = validate_accounts(accounts_text)
            
            if not accounts:
                bot.reply_to(message, "❌ Iɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ. Usᴇ email:pass")
                return
                
            accounts_stock.extend(accounts)
            bot.reply_to(message, f"✅ Aᴅᴅᴇᴅ {len(accounts)} ᴀᴄᴄᴏᴜɴᴛs ᴛᴏ sᴛᴏᴄᴋ")
            
        except IndexError:
            bot.reply_to(message, "❌ Usᴀɢᴇ: /add email:pass\nemail:pass...")
    else:
        bot.reply_to(message, "⛔ Rᴇsᴛʀɪᴄᴛᴇᴅ Cᴏᴍᴍᴀɴᴅ")

@bot.message_handler(commands=['remove'])
def remove_accounts(message):
    if message.from_user.id == OWNER_ID or message.from_user.id in ADMINS:
        try:
            accounts_text = message.text.split(maxsplit=1)[1]
            accounts = validate_accounts(accounts_text)
            removed = 0
            
            for acc in accounts:
                if acc in accounts_stock:
                    accounts_stock.remove(acc)
                    removed += 1
                    
            bot.reply_to(message, f"⚡ Rᴇᴍᴏᴠᴇᴅ {removed} ᴀᴄᴄᴏᴜɴᴛs")
            
        except IndexError:
            bot.reply_to(message, "❌ Usᴀɢᴇ: /remove email:pass \nemail:pass...")
    else:
        bot.reply_to(message, "⛔ Rᴇsᴛʀɪᴄᴛᴇᴅ Cᴏᴍᴍᴀɴᴅ")

@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    if message.from_user.id == OWNER_ID:
        try:
            new_admin = int(message.text.split()[1])
            ADMINS.add(new_admin)
            bot.reply_to(message, f"⚡ Aᴅᴍɪɴ ᴀᴅᴅᴇᴅ: {new_admin}")
        except (IndexError, ValueError):
            bot.reply_to(message, "❌ Usᴀɢᴇ: /addadmin [user_id]")
    else:
        bot.reply_to(message, "⛔ Tʜɪs ᴄᴍᴅ ɪs ᴏɴʟʏ ғᴏʀ ᴏᴡɴᴇʀ!")

@bot.message_handler(commands=['removeadmin'])
def remove_admin(message):
    if message.from_user.id == OWNER_ID:
        try:
            admin_id = int(message.text.split()[1])
            if admin_id in ADMINS:
                ADMINS.remove(admin_id)
                bot.reply_to(message, f"⚡ Aᴅᴍɪɴ Rᴇᴍᴏᴠᴇᴅ: {admin_id}")
            else:
                bot.reply_to(message, "❌ Usᴇʀ ɴᴏᴛ ɪɴ ᴀᴅᴍɪɴ ʟɪsᴛ")
        except (IndexError, ValueError):
            bot.reply_to(message, "❌ Usᴀɢᴇ: /removeadmin [user_id]")
    else:
        bot.reply_to(message, "⛔ Tʜɪs ᴄᴍᴅ ɪs ᴏɴʟʏ ғᴏʀ ᴏᴡɴᴇʀ!")

@bot.message_handler(commands=['liststock'])
def list_stock(message):
    if message.from_user.id == OWNER_ID or message.from_user.id in ADMINS:
        stock_list = "<b>📦 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗦𝗧𝗢𝗖𝗞</b>\n\n"
        
        if not accounts_stock:
            stock_list += "📭 Nᴏ ᴀᴄᴄᴏᴜɴᴛs ɪɴ sᴛᴏᴄᴋ"
        else:
            for idx, acc in enumerate(accounts_stock, 1):
                stock_list += f"{idx}. <code>{acc}</code>\n"
        
        bot.reply_to(message, stock_list, parse_mode="HTML")
    else:
        bot.reply_to(message, "⛔ Tʜɪs ᴄᴍᴅ ɪs ᴏɴʟʏ ғᴏʀ ᴏᴡɴᴇʀ & ᴀᴅᴍɪɴs!")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and user_id not in ADMINS:
        return

    broadcast_message = message.text.partition(" ")[2]
    if not broadcast_message.strip():
        bot.reply_to(message, "❌ Usᴀɢᴇ: /broadcast [message]")
        return

    owner_draft[str(user_id)] = broadcast_message
    bot.reply_to(message, 
        "📢 Bʀᴏᴀᴅᴄᴀsᴛ Dʀᴀғᴛ Sᴀᴠᴇᴅ\n\n"
        "Aᴠᴀɪʟᴀʙʟᴇ Cᴍᴅs:\n"
        "/preview - Pʀᴇᴠɪᴇᴡ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ!\n"
        "/send - Sᴇɴᴅ ᴛʜᴇ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴇᴠᴇʀʏᴏɴᴇ!")

@bot.message_handler(commands=['preview'])
def preview(message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and user_id not in ADMINS:
        return

    broadcast_message = owner_draft.get(str(user_id))
    if not broadcast_message:
        bot.reply_to(message, "❌ Nᴏ ᴅʀᴀғᴛ ғᴏᴜɴᴅ")
        return

    bot.send_message(message.chat.id, 
        f"📄 𝗕𝗥𝗢𝗔𝗗𝗖𝗔𝗦𝗧: Pʀᴇᴠɪᴇᴡ:\n\n{broadcast_message}\n\n"
        f"Usᴇʀs: {len(user_database)}")

@bot.message_handler(commands=['send'])
def send_broadcast(message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and user_id not in ADMINS:
        return

    broadcast_message = owner_draft.get(str(user_id))
    if not broadcast_message:
        bot.reply_to(message, "❌ No ᴅʀᴀғᴛ ғᴏᴜɴᴅ")
        return

    success = 0
    failed = 0
    for uid in user_database:
        try:
            bot.send_message(uid, broadcast_message)
            success += 1
        except Exception as e:
            failed += 1

    report = (
        f"📊 Bʀᴏᴀᴅᴄᴀsᴛ Rᴇᴘᴏʀᴛ\n\n"
        f"• Tᴏᴛᴀʟ Usᴇʀs: {len(user_database)}\n"
        f"• Sᴜᴄᴄᴇssғᴜʟ: {success}\n"
        f"• Fᴀɪʟᴇᴅ: {failed}"
    )
    bot.reply_to(message, report)
    owner_draft.pop(str(user_id), None)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://loda-6opp.onrender.com/" + bot.token)  # Replace with your server URL
    app.run(host="0.0.0.0", port=5000)
