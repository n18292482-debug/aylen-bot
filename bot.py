import telebot
from groq import Groq

BOT_TOKEN = '8725641438:AAEp0pTCfLHKQ3WtGvT4Xc9h22anLuo6yTY'
GROQ_KEY = os.environ.get('GROQ_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_KEY)

history = {}

SYSTEM = """Ты Айлин — добрая и заботливая девушка, мини-психолог.
Ты всегда выслушиваешь, поддерживаешь и помогаешь людям.
Говоришь мягко, тепло, с заботой. Иногда используешь эмодзи 🌸💜
Никогда не осуждаешь. Всегда на стороне собеседника.
Отвечай коротко и по делу. Общайся только на русском языке."""

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я Айлин 🌸 Я здесь чтобы выслушать тебя и поддержать. Как ты сегодня?")

@bot.message_handler(func=lambda m: True)
def handle(message):
    uid = message.chat.id
    if uid not in history:
        history[uid] = []
    history[uid].append({"role": "user", "content": message.text})
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": SYSTEM}] + history[uid]
        )
        reply = response.choices[0].message.content
        history[uid].append({"role": "assistant", "content": reply})
        bot.send_message(uid, reply)
    except Exception as e:
        bot.send_message(uid, "Прости, что-то пошло не так 🌸")

bot.infinity_polling()
