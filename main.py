from telebot import TeleBot, types

TOKEN = '7961055236:AAHoGcIwo91sHc12cV0VSCaWobYoRTgOrMc' 
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_options(message):
    """Send a welcome message and ask for phone number."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    phone_button = types.KeyboardButton("📞 Telefon raqamingizni yuboring", request_contact=True)
    markup.add(phone_button)
    bot.send_message(
        chat_id=message.chat.id,
        text="Iltimos, telefon raqamingizni yuboring:",
        reply_markup=markup
    )

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """Handle the contact information sent by the user."""
    phone_number = message.contact.phone_number
    bot.send_message(chat_id=message.chat.id, text=f"Sizning telefon raqamingiz: {phone_number}")
    send_main_options(message)

def send_main_options(message):
    """Send main options after receiving the phone number."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("🛒 Buyurtma berish"),
        types.KeyboardButton("📦 Buyurtmalarim"),
        types.KeyboardButton("🖊 Fikr bildirish"),
        types.KeyboardButton("🍽 Menyu"),
        types.KeyboardButton("⚙️ Sozlamalar")
    ]
    markup.add(*buttons)
    bot.send_message(
        chat_id=message.chat.id,
        text="Quyidagilardan birini tanlang:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "🛒 Buyurtma berish")
def order_options(message):
    """Send order-related options."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        types.KeyboardButton("📍 Geo-joylashuvni yuborish", request_location=True),
        types.KeyboardButton("🔙 Orqaga")
    ]
    markup.add(*buttons)
    bot.send_message(chat_id=message.chat.id, text="Buyurtma berish uchun geo-joylashuvni jo'nating yoki orqaga qayting:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🍽 Menyu")
def send_image(message):
    """Send an image when the menu option is selected."""
    with open("menyu.jpg", "rb") as img:
        bot.send_photo(message.chat.id, img, caption='buyurtma berish uchun shu rasmdagi biror bir mahsulotni tanlang')
    send_main_options(message) 

@bot.message_handler(func=lambda message: True)
def handle_options(message):
    """Handle user responses from the menu."""
    if message.text == "📦 Buyurtmalarim":
        bot.send_message(chat_id=message.chat.id, text="Sizning buyurtmalaringiz ko'rib chiqilmoqda.")
    elif message.text == "🖊 Fikr bildirish":
        bot.send_message(chat_id=message.chat.id, text="Fikr bildirish uchun xabar yuboring.")
    elif message.text == "⚙️ Sozlamalar":
        bot.send_message(chat_id=message.chat.id, text="Sozlamalar bo'limida hozircha o'zgarishlar yo'q.")
    elif message.text == "🔙 Orqaga":
        send_main_options(message)
    else:
        bot.send_message(chat_id=message.chat.id, text="Sizning javobingiz qabul qilindi.")

if __name__ == "__main__":
    bot.polling()
