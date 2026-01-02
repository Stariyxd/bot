# bot.py
import telebot
from telebot import types
import datetime
import os

# Токен из Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

# Хранение состояний
user_states = {}

# ================================
# /start
# ================================
@bot.message_handler(commands=['start'])
def start(message):
    # Сбрасываем состояние
    user_states[message.chat.id] = None
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📰 Подать новость"))
    markup.add(types.KeyboardButton("💼 Откликнуться на вакансию"))
    markup.add(types.KeyboardButton("❓ Задать вопрос"))
    
    text = """👋 <b>Привет!</b>

Ты написал в редакцию <b>SHUMAHER NEWS</b> — 
первого новостного канала о CPM.

📰 <b>Подать новость</b> — расскажи о событии
💼 <b>Вакансии</b> — откликнись в команду
❓ <b>Вопрос</b> — задай любой вопрос

━━━━━━━━━━━━━━━━━━━━━

📺 @shumaher_news
💬 @shumaher_news_chat"""
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# ================================
# /myid — узнать свой ID
# ================================
@bot.message_handler(commands=['myid'])
def my_id(message):
    bot.send_message(message.chat.id, f"Твой ID: <code>{message.chat.id}</code>", parse_mode='HTML')

# ================================
# /reply — ответить пользователю (ТОЛЬКО ДЛЯ АДМИНА)
# ================================
@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    # Проверяем что это админ
    if message.chat.id != ADMIN_CHAT_ID:
        bot.send_message(message.chat.id, "⛔ Нет доступа")
        return
    
    try:
        # Получаем текст после /reply
        full_text = message.text
        
        # Убираем команду /reply
        if full_text.startswith('/reply '):
            full_text = full_text[7:]  # Убираем "/reply "
        else:
            bot.send_message(ADMIN_CHAT_ID, 
                "❌ Неверный формат!\n\n"
                "Правильно:\n"
                "<code>/reply 123456789 Текст ответа</code>", 
                parse_mode='HTML')
            return
        
        # Ищем первый пробел — разделяем ID и текст
        space_index = full_text.find(' ')
        
        if space_index == -1:
            bot.send_message(ADMIN_CHAT_ID, 
                "❌ Не указан текст ответа!\n\n"
                "Правильно:\n"
                "<code>/reply 123456789 Текст ответа</code>", 
                parse_mode='HTML')
            return
        
        user_id_str = full_text[:space_index]
        reply_text = full_text[space_index + 1:]
        
        user_id = int(user_id_str)
        
        if not reply_text.strip():
            bot.send_message(ADMIN_CHAT_ID, "❌ Текст ответа пустой!")
            return
        
        # Отправляем ответ пользователю
        answer = f"""📬 <b>Ответ от SHUMAHER NEWS:</b>

{reply_text}

━━━━━━━━━━━━━━━━━━━━━

📺 @shumaher_news
💬 @shumaher_news_chat"""
        
        bot.send_message(user_id, answer, parse_mode='HTML')
        bot.send_message(ADMIN_CHAT_ID, f"✅ Ответ отправлен пользователю!")
        
    except ValueError:
        bot.send_message(ADMIN_CHAT_ID, 
            "❌ Неверный ID!\n\n"
            "ID должен быть числом.\n"
            "Пример: <code>/reply 123456789 Привет!</code>", 
            parse_mode='HTML')
    except Exception as e:
        bot.send_message(ADMIN_CHAT_ID, f"❌ Ошибка: {e}")

# ================================
# Подать новость
# ================================
@bot.message_handler(func=lambda m: m.text == "📰 Подать новость")
def submit_news(message):
    user_states[message.chat.id] = "waiting_news"
    
    text = """📰 <b>ПОДАТЬ НОВОСТЬ</b>

Напиши <b>одним сообщением</b>:

1️⃣ Что случилось?
2️⃣ Сервер (1, 2, 3...)
3️⃣ Локация
4️⃣ Когда?
5️⃣ Твой ник

📎 Прикрепи видео/скриншот!"""
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("◀️ Назад"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# ================================
# Вакансии
# ================================
@bot.message_handler(func=lambda m: m.text == "💼 Откликнуться на вакансию")
def apply_job(message):
    user_states[message.chat.id] = "waiting_job"
    
    text = """💼 <b>ВАКАНСИИ</b>

🎤 Ведущие
📹 Корреспонденты
🎮 Операторы
📝 Сценарист
🎨 Дизайнер
📱 SMM

📋 Подробности: @shumaher_news_job

━━━━━━━━━━━━━━━━━━━━━

<b>Напиши:</b>
1. Вакансия
2. Ник в игре
3. Возраст
4. Есть микрофон?
5. Часов в неделю
6. Почему хочешь к нам

🎤 Ведущим — запиши голосовое 30 сек!"""
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("◀️ Назад"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# ================================
# Вопрос
# ================================
@bot.message_handler(func=lambda m: m.text == "❓ Задать вопрос")
def ask_question(message):
    user_states[message.chat.id] = "waiting_question"
    
    text = """❓ <b>ВОПРОС</b>

Напиши вопрос — ответим в течение 24 часов.

Срочно? Пиши в @shumaher_news_chat"""
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("◀️ Назад"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# ================================
# Назад
# ================================
@bot.message_handler(func=lambda m: m.text == "◀️ Назад")
def go_back(message):
    user_states[message.chat.id] = None
    start(message)

# ================================
# Обработка ВСЕХ остальных сообщений
# ================================
@bot.message_handler(func=lambda m: True, content_types=['text', 'photo', 'video', 'document', 'voice', 'video_note'])
def handle_message(message):
    # Пропускаем команды — они уже обработаны выше
    if message.text and message.text.startswith('/'):
        return
    
    # Для админа без состояния — не реагируем на обычные сообщения
    if message.chat.id == ADMIN_CHAT_ID:
        state = user_states.get(message.chat.id)
        if state is None:
            return  # Админ просто пишет что-то, игнорируем
    
    state = user_states.get(message.chat.id)
    
    if state is None:
        bot.send_message(message.chat.id, "Выбери пункт меню 👇")
        return
    
    if state == "waiting_news":
        label = "📰 НОВОСТЬ"
    elif state == "waiting_job":
        label = "💼 ВАКАНСИЯ"
    elif state == "waiting_question":
        label = "❓ ВОПРОС"
    else:
        return
    
    user = message.from_user
    username = f"@{user.username}" if user.username else "нет username"
    name = user.first_name or "Без имени"
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    
    admin_text = f"""━━━━━━━━━━━━━━━━━━━━━
<b>{label}</b>
━━━━━━━━━━━━━━━━━━━━━

👤 <b>Имя:</b> {name}
📱 <b>Username:</b> {username}
🆔 <b>ID:</b> <code>{user.id}</code>
🕐 <b>Время:</b> {now}

━━━━━━━━━━━━━━━━━━━━━

💬 <b>Ответить:</b>
<code>/reply {user.id} Ваш текст</code>

━━━━━━━━━━━━━━━━━━━━━"""
    
    try:
        bot.send_message(ADMIN_CHAT_ID, admin_text, parse_mode='HTML')
        bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")
    
    # Сбрасываем состояние
    user_states[message.chat.id] = None
    
    # Возвращаем меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📰 Подать новость"))
    markup.add(types.KeyboardButton("💼 Откликнуться на вакансию"))
    markup.add(types.KeyboardButton("❓ Задать вопрос"))
    
    bot.send_message(message.chat.id, "✅ Принято! Ответим в течение 24 часов.", reply_markup=markup)

# ================================
# Запуск
# ================================
def start_bot():
    print("🤖 SHUMAHER NEWS Bot запущен!")
    print(f"ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")
    bot.infinity_polling()

if __name__ == "__main__":
    start_bot()
