import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from groq import Groq
from PIL import Image, ImageFilter
import io

MODELO = "llama-3.3-70b-versatile"

def get_tokens():
    token = os.getenv("8743591475:AAGRm04hq-E9fIiJx205VQsU2VqEoNyxD9o")
    groq_key = os.getenv("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")
    
    if not token:
        raise ValueError("TELEGRAM_TOKEN não configurada!")
    if not groq_key:
        raise ValueError("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")
    
    return token, groq_key

async def start(update, context):
    await update.message.reply_text(
        "🤖 Bot com IA avançada!\n\n"
        "📝 Envie texto para análise\n"
        "📸 Envie imagens para análise\n"
        "🎥 Envie vídeos para análise\n\n"
        "Comandos:\n"
        "/blur - desfocar imagem\n"
        "/resize - redimensionar\n"
        "/rotate - girar imagem"
    )

async def responder_texto(update, context):
    msg = update.message.text
    await update.message.chat.send_action(action="typing")
    try:
        _, groq_key = get_tokens()
        cliente = Groq(api_key=groq_key)
        resposta = cliente.chat.completions.create(
            model=MODELO,
            messages=[{"role": "user", "content": msg}]
        )
        await update.message.reply_text(resposta.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")

async def responder_imagem(update, context):
    await update.message.chat.send_action(action="typing")
    try:
        file = await update.message.photo[-1].get_file()
        img_bytes = await file.download_as_bytearray()
        
        _, groq_key = get_tokens()
        cliente = Groq(api_key=groq_key)
        resposta = cliente.chat.completions.create(
            model=MODELO,
            messages=[{
                "role": "user",
                "content": "Analise esta imagem e descreva o que você vê em detalhes."
            }]
        )
        
        await update.message.reply_text(f"📸 Análise:\n{resposta.choices[0].message.content}")
    except Exception as e:
        await update.message.reply_text(f"Erro ao processar imagem: {e}")

async def responder_video(update, context):
    await update.message.chat.send_action(action="typing")
    try:
        file = await update.message.video.get_file()
        await update.message.reply_text("📹 Vídeo recebido! Processando...")
        
        _, groq_key = get_tokens()
        cliente = Groq(api_key=groq_key)
        resposta = cliente.chat.completions.create(
            model=MODELO,
            messages=[{
                "role": "user",
                "content": "Descreva o que você vê neste vídeo."
            }]
        )
        
        await update.message.reply_text(f"Análise: {resposta.choices[0].message.content}")
    except Exception as e:
        await update.message.reply_text(f"Erro ao processar vídeo: {e}")

async def blur_imagem(update, context):
    try:
        if not update.message.reply_to_message or not update.message.reply_to_message.photo:
            await update.message.reply_text("Responda a uma imagem com /blur")
            return
        
        file = await update.message.reply_to_message.photo[-1].get_file()
        img_bytes = await file.download_as_bytearray()
        img = Image.open(io.BytesIO(img_bytes))
        
        img_blur = img.filter(ImageFilter.GaussianBlur(radius=10))
        
        output = io.BytesIO()
        img_blur.save(output, format="PNG")
        output.seek(0)
        
        await update.message.reply_photo(photo=output)
    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")

async def resize_imagem(update, context):
    try:
        if not context.args:
            await update.message.reply_text("Use: /resize 400 300")
            return
        
        if not update.message.reply_to_message or not update.message.reply_to_message.photo:
            await update.message.reply_text("Responda a uma imagem com /resize")
            return
        
        width, height = int(context.args[0]), int(context.args[1])
        
        file = await update.message.reply_to_message.photo[-1].get_file()
        img_bytes = await file.download_as_bytearray()
        img = Image.open(io.BytesIO(img_bytes))
        
        img_resized = img.resize((width, height))
        
        output = io.BytesIO()
        img_resized.save(output, format="PNG")
        output.seek(0)
        
        await update.message.reply_photo(photo=output)
    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")

async def rotate_imagem(update, context):
    try:
        if not context.args:
            await update.message.reply_text("Use: /rotate 90")
            return
        
        if not update.message.reply_to_message or not update.message.reply_to_message.photo:
            await update.message.reply_text("Responda a uma imagem com /rotate")
            return
        
        angle = int(context.args[0])
        
        file = await update.message.reply_to_message.photo[-1].get_file()
        img_bytes = await file.download_as_bytearray()
        img = Image.open(io.BytesIO(img_bytes))
        
        img_rotated = img.rotate(angle, expand=True)
        
        output = io.BytesIO()
        img_rotated.save(output, format="PNG")
        output.seek(0)
        
        await update.message.reply_photo(photo=output)
    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")

def main():
    token, _ = get_tokens()
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("blur", blur_imagem))
    app.add_handler(CommandHandler("resize", resize_imagem))
    app.add_handler(CommandHandler("rotate", rotate_imagem))
    
    app.add_handler(MessageHandler(filters.PHOTO, responder_imagem))
    app.add_handler(MessageHandler(filters.VIDEO, responder_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_texto))
    
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
