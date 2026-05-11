
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from groq import Groq

# ==================================================
# PEGA AS CHAVES DAS VARIÁVEIS DE AMBIENTE
# ==================================================
TELEGRAM_TOKEN = os.environ.get("8743591475:AAGkTTCamdOgbzneh6wULEJfAIkM9U60GSI")
GROQ_API_KEY = os.environ.get("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")

MODELO = "llama-3.1-8b-instant"

# Inicializa o cliente Groq
cliente = Groq(api_key=GROQ_API_KEY)

# ==================================================
# COMANDOS DO BOT
# ==================================================

async def start(update, context):
    await update.message.reply_text(
        "🤖 *Bot funcionando!*\n\n"
        f"✅ Modelo: `{MODELO}`\n"
        "⚡ IA gratuita via Groq\n"
        "🟢 Rodando 24/7\n\n"
        "Me envie qualquer mensagem!",
        parse_mode="Markdown"
    )

async def responder(update, context):
    msg = update.message.text
    print(f"👤 Usuário: {msg}")
    
    await update.message.chat.send_action(action="typing")
    
    try:
        resposta = cliente.chat.completions.create(
            model=MODELO,
            messages=[
                {"role": "system", "content": "Você é um assistente amigável que responde em português."},
                {"role": "user", "content": msg}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        texto = resposta.choices[0].message.content
        await update.message.reply_text(texto)
        print(f"🤖 Resposta enviada")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        await update.message.reply_text(f"❌ Erro: {str(e)}")

# ==================================================
# INICIALIZAÇÃO
# ==================================================

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    
    print("=" * 50)
    print("✅ BOT INICIADO COM SUCESSO!")
    print(f"🤖 Modelo: {MODELO}")
    print("📱 Bot rodando 24/7!")
    print("=" * 50)
    
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
