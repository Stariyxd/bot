# bot.py
# SHUMAHER NEWS Bot

import telebot
from telebot import types
import datetime

# Токен от @BotFather
BOT_TOKEN = "8335314646:AAHQa_vdn8x7sjuL5VAM6wM5HbOZuMsvifE"

# ID чата/группы куда пересылать заявки
# Узнать свой ID: напиши боту @userinfobot
ADMIN_CHAT_ID = 3528774795/8  # Замени на свой ID

bot = telebot.TeleBot(BOT_TOKEN)

# Хранение состояний пользователей
user_states = {}

# ================================
# КОМАНДА /start
# ================================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📰 Подать новость")
    btn2 = types.KeyboardButton("💼 Откликнуться на вакансию")
    btn3 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    
    text = """👋 <b>Привет!</b>

Ты написал в редакцию <b>SHUMAHER NEWS</b> — 
первого новостного канала о CPM.

Выбери, что тебе нужно:

📰 <b>Подать новость</b> — расскажи о событии в игре
💼 <b>Вакансии</b> — откликнись на позицию в команде
❓ <b>Вопрос</b> — задай любой вопрос

━━━━━━━━━━━━━━━━━━━━━

📺 Канал: @shumaher_news
💬 Чат: @shumaher_news_chat
💼 Вакансии: @shumaher_news_job"""
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# ================================
# КНОПКА "Подать новость"
# ================================
@bot.message_handler(func=lambda m: m.text == "📰 Подать новость")
def submit_news(message):
    user_states[message.chat.id] = "waiting_news"
    
    text = """📰 <b>ПОДАТЬ НОВОСТЬ</b>

Напиши <b>одним сообщением</b>:

1️⃣ Что случилось?
2️⃣ Сервер (1, 2, 3, Европа...)
3️⃣ Локация (где именно)
4️⃣ Когда это было?
5️⃣ Твой ник (для упоминания в эфире)

📎 Прикрепи видео или скриншот!

━━━━━━━━━━━━━━━━━━━━━

<i>Отправь всё следующим сообщением</i> 👇"""
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("◀️ Назад"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# ================================
# КНОПКА "Откликнуться на вакансию"
# ================================
@bot.message_handler(func=lambda m: m.text == "💼 Откликнуться на вакансию")
def apply_job(message):
    user_states[message.chat.id] = "waiting_job"
    
    text = """💼 <b>ОТКЛИКНУТЬСЯ НА ВАКАНСИЮ</b>

Мы ищем:
🎤 Ведущих
📹 Корреспондентов
🎮 Операторов
📝 Сценариста
🎨 Дизайнера
📱 SMM-менеджера
📩 Модератора

📋 Подробности: @shumaher_news_job

━━━━━━━━━━━━━━━━━━━━━

Чтобы откликнуться, напиши:

1️⃣ На какую вакансию претендуешь
2️⃣ Твой ник в игре
3️⃣ Возраст
4️⃣ Есть ли микрофон
5️⃣ Сколько часов в неделю готов уделять
6️⃣ Почему хочешь к нам
7️⃣ Опыт (если есть)

🎤 <b>Для ведущих/корреспондентов:</b>
Запиши голосовое 30 сек — прочитай любой текст!

━━━━━━━━━━━━━━━━━━━━━

<i>Отправь всё следующим сообщением</i> 👇"""
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("◀️ Назад"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# ================================
# КНОПКА "Задать вопрос"
# ================================
@bot.message_handler(func=lambda m: m.text == "❓ Задать вопрос")
def ask_question(message):
    user_states[message.chat.id] = "waiting_question"
    
    text = """❓ <b>ЗАДАТЬ ВОПРОС</b>

Напиши свой вопрос, и мы ответим 
в течение 24 часов.

Если срочно — пиши в чат @shumaher_news_chat

━━━━━━━━━━━━━━━━━━━━━

<i>Отправь вопрос следующим сообщением</i> 👇"""
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("◀️ Назад"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# ================================
# КНОПКА "Назад"
# ================================
@bot.message_handler(func=lambda m: m.text == "◀️ Назад")
def go_back(message):
    user_states[message.chat.id] = None
    start(message)

# ================================
# ОБРАБОТКА СООБЩЕНИЙ
# ================================
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'voice', 'video_note'])
def handle_message(message):
    state = user_states.get(message.chat.id)
    
    if state is None:
        # Если пользователь просто написал что-то
        bot.send_message(message.chat.id, "Выбери пункт меню 👇")
        return
    
    # Определяем тип заявки
    if state == "waiting_news":
        label = "📰 НОВОСТЬ"
        emoji = "📰"
    elif state == "waiting_job":
        label = "💼 ВАКАНСИЯ"
        emoji = "💼"
    elif state == "waiting_question":
        label = "❓ ВОПРОС"
        emoji = "❓"
    else:
        return
    
    # Информация о пользователе
    user = message.from_user
    username = f"@{user.username}" if user.username else "нет username"
    name = user.first_name
    if user.last_name:
        name += f" {user.last_name}"
    
    # Формируем сообщение для админа
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    
    admin_text = f"""━━━━━━━━━━━━━━━━━━━━━
{emoji} <b>{label}</b>
━━━━━━━━━━━━━━━━━━━━━

👤 <b>От:</b> {name}
📱 <b>Username:</b> {username}
🆔 <b>ID:</b> <code>{user.id}</code>
🕐 <b>Время:</b> {now}

━━━━━━━━━━━━━━━━━━━━━
"""
    
    # Отправляем админу
    bot.send_message(ADMIN_CHAT_ID, admin_text, parse_mode='HTML')
    
    # Пересылаем оригинальное сообщение
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
    
    # Подтверждение пользователю
    confirm_text = f"""✅ <b>Спасибо!</b>

Твоя заявка принята и передана в редакцию.

Мы ответим в течение 24 часов.

━━━━━━━━━━━━━━━━━━━━━

📺 Канал: @shumaher_news
💬 Чат: @shumaher_news_chat"""
    
    # Сбрасываем состояние
    user_states[message.chat.id] = None
    
    # Возвращаем главное меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📰 Подать новость"))
    markup.add(types.KeyboardButton("💼 Откликнуться на вакансию"))
    markup.add(types.KeyboardButton("❓ Задать вопрос"))
    
    bot.send_message(message.chat.id, confirm_text, parse_mode='HTML', reply_markup=markup)

# ================================
# КОМАНДА ДЛЯ ОТВЕТА (для админа)
# ================================
@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    # Только для админа
    if message.chat.id != ADMIN_CHAT_ID:
        return
    
    # Формат: /reply USER_ID текст ответа
    try:
        parts = message.text.split(' ', 2)
        user_id = int(parts[1])
        reply_text = parts[2]
        
        text = f"""📬 <b>Ответ от SHUMAHER NEWS:</b>

{reply_text}

━━━━━━━━━━━━━━━━━━━━━

📺 Канал: @shumaher_news"""
        
        bot.send_message(user_id, text, parse_mode='HTML')
        bot.send_message(ADMIN_CHAT_ID, f"✅ Ответ отправлен пользователю {user_id}")
    except:
        bot.send_message(ADMIN_CHAT_ID, "❌ Ошибка. Формат: /reply USER_ID текст")

# ================================
# ЗАПУСК БОТА
# ================================
print("Бот запущен...")
bot.infinity_polling()