import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from groq import Groq

TELEGRAM_TOKEN = "8743591475:AAGRm04hq-E9fIiJx205VQsU2VqEoNyxD9o"
GROQ_API_KEY = "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"

MODELO = "llama-3.3-70b-versatile"
cliente = Groq(api_key=GROQ_API_KEY)

async def start(update, context):
    await update.message.reply_text("🤖 Bot funcionando 24/7! Me mande qualquer mensagem.")

async def responder(update, context):
    msg = update.message.text
    await update.message.chat.send_action(action="typing")
    try:
        resposta = cliente.chat.completions.create(
            model=MODELO,
            messages=[{"role": "user", "content": msg}]
        )
        await update.message.reply_text(resposta.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
