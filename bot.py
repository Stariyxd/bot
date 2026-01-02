# bot.py
import telebot
from telebot import types
import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

# ================================
# ВСЕ КОМАНДЫ СНАЧАЛА
# ================================

@bot.message_handler(commands=['start'])
def cmd_start(message):
    user_states[message.chat.id] = None
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📰 Подать новость"))
    markup.add(types.KeyboardButton("💼 Откликнуться на вакансию"))
    markup.add(types.KeyboardButton("❓ Задать вопрос"))
    
    text = """👋 <b>Привет!</b>

Ты написал в редакцию <b>SHUMAHER NEWS</b>

📰 Подать новость
💼 Откликнуться на вакансию  
❓ Задать вопрос

📺 @shumaher_news"""
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)


@bot.message_handler(commands=['myid'])
def cmd_myid(message):
    bot.send_message(message.chat.id, f"Твой ID: <code>{message.chat.id}</code>\nADMIN_ID: <code>{ADMIN_CHAT_ID}</code>", parse_mode='HTML')


@bot.message_handler(commands=['reply'])
def cmd_reply(message):
    # Логируем что команда получена
    print(f"REPLY command from {message.chat.id}")
    
    if message.chat.id != ADMIN_CHAT_ID:
        bot.send_message(message.chat.id, "⛔ Нет доступа")
        return
    
    try:
        text = message.text[7:]  # Убираем "/reply "
        
        if ' ' not in text:
            bot.send_message(message.chat.id, "❌ Формат: /reply ID текст")
            return
        
        parts = text.split(' ', 1)
        user_id = int(parts[0])
        reply_text = parts[1]
        
        bot.send_message(user_id, f"📬 <b>Ответ SHUMAHER NEWS:</b>\n\n{reply_text}", parse_mode='HTML')
        bot.send_message(message.chat.id, "✅ Отправлено!")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")


# ================================
# КНОПКИ МЕНЮ
# ================================

@bot.message_handler(func=lambda m: m.text == "📰 Подать новость")
def btn_news(message):
    user_states[message.chat.id] = "news"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("◀️ Назад"))
    bot.send_message(message.chat.id, "📰 Напиши новость:", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "💼 Откликнуться на вакансию")
def btn_job(message):
    user_states[message.chat.id] = "job"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("◀️ Назад"))
    bot.send_message(message.chat.id, "💼 Напиши заявку на вакансию:\n\n1. Вакансия\n2. Ник\n3. Возраст\n4. Микрофон?\n5. Почему хочешь к нам", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "❓ Задать вопрос")
def btn_question(message):
    user_states[message.chat.id] = "question"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("◀️ Назад"))
    bot.send_message(message.chat.id, "❓ Напиши вопрос:", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "◀️ Назад")
def btn_back(message):
    user_states[message.chat.id] = None
    cmd_start(message)


# ================================
# ОБРАБОТКА СООБЩЕНИЙ (В КОНЦЕ!)
# ================================

@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'voice'])
def handle_all(message):
    # Игнорируем команды
    if message.text and message.text.startswith('/'):
        print(f"Ignoring command: {message.text}")
        return
    
    state = user_states.get(message.chat.id)
    
    # Нет состояния — просим выбрать меню
    if not state:
        # Для админа не спамим
        if message.chat.id == ADMIN_CHAT_ID:
            return
        bot.send_message(message.chat.id, "Выбери пункт меню 👇")
        return
    
    # Определяем тип
    if state == "news":
        label = "📰 НОВОСТЬ"
    elif state == "job":
        label = "💼 ВАКАНСИЯ"
    elif state == "question":
        label = "❓ ВОПРОС"
    else:
        return
    
    # Данные пользователя
    user = message.from_user
    username = f"@{user.username}" if user.username else "нет"
    name = user.first_name or "Аноним"
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    
    # Сообщение админу
    admin_msg = f"""━━━━━━━━━━━━━━━━━━
<b>{label}</b>
━━━━━━━━━━━━━━━━━━

👤 {name}
📱 {username}
🆔 <code>{user.id}</code>
🕐 {now}

━━━━━━━━━━━━━━━━━━
<code>/reply {user.id} ответ</code>
━━━━━━━━━━━━━━━━━━"""
    
    try:
        bot.send_message(ADMIN_CHAT_ID, admin_msg, parse_mode='HTML')
        bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
    except Exception as e:
        print(f"Error: {e}")
    
    # Сброс и ответ пользователю
    user_states[message.chat.id] = None
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📰 Подать новость"))
    markup.add(types.KeyboardButton("💼 Откликнуться на вакансию"))
    markup.add(types.KeyboardButton("❓ Задать вопрос"))
    
    bot.send_message(message.chat.id, "✅ Принято!", reply_markup=markup)


# ================================
# ЗАПУСК
# ================================

def start_bot():
    print("=" * 40)
    print("SHUMAHER NEWS Bot")
    print(f"ADMIN_CHAT_ID = {ADMIN_CHAT_ID}")
    print("=" * 40)
    bot.infinity_polling()

if __name__ == "__main__":
    start_bot()
