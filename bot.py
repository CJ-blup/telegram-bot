from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your bot token
BOT_TOKEN = "8282451151:AAEUKXQC84WXT1dhfvAQihsoMLFzvEdgNV4"

# Store per-user data
# user_data[user_id] = {"salary": 1255, "expenses": [(expense, remaining_balance), ...]}
user_data = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"salary": 1255, "expenses": []}
    await update.message.reply_text(
        "Hello! 👋 Send any expense amount and I will deduct it from 1255.\n"
        "Use /history to see all expenses and remaining balance.\n"
        "Use /newsalary <amount> to reset the salary."
    )

# Show expense history
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data or not user_data[user_id]["expenses"]:
        await update.message.reply_text("You have no expenses recorded yet.")
        return

    msg = f"💰 Expense history (Current balance: {user_data[user_id]['salary']}):\n"
    for expense, remaining in user_data[user_id]["expenses"]:
        msg += f"- Expense: {expense} → Remaining balance: {remaining}\n"
    await update.message.reply_text(msg)

# Deduct expenses
async def deduct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"salary": 1255, "expenses": []}
    try:
        expense = int(update.message.text)
        remaining_balance = user_data[user_id]["salary"] - expense
        user_data[user_id]["salary"] = remaining_balance
        user_data[user_id]["expenses"].append((expense, remaining_balance))
        await update.message.reply_text(
            f"💸 Deducted: {expense}\nCurrent balance: {remaining_balance}"
        )
    except ValueError:
        await update.message.reply_text("❌ Please send a valid expense amount.")

# Set a new salary
async def newsalary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /newsalary <amount>")
        return
    try:
        new_salary = int(context.args[0])
        user_data[user_id] = {"salary": new_salary, "expenses": []}
        await update.message.reply_text(f"✅ New salary set to {new_salary}. Expenses cleared.")
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number for the new salary.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("newsalary", newsalary))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, deduct))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
