from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your new token (NEVER share it publicly!)
BOT_TOKEN = "8282451151:AAEUKXQC84WXT1dhfvAQihsoMLFzvEdgNV4"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! 👋 Enter Expenditure."
    )

# Subtraction logic
async def subtract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        num = int(update.message.text)
        result = 1255 - num
        await update.message.reply_text(f"1255 - {num} = {result}")
    except ValueError:
        await update.message.reply_text("❌ Please send a valid number.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, subtract))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
