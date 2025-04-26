import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import telebot
from dotenv import load_dotenv

# Importar todos los módulos
from modules.sqli_scanner import scan_url
from modules.nmap_scanner import scan_host, scan_host_full, scan_host_stealth, scan_host_vuln
from modules.injector import extract_database_name
from modules.bruteforcer import bruteforce_login
from modules.form_scanner import scan_forms
from modules.logger import save_log
from modules.exploit_suggester import suggest_exploits
from modules.utils.helpers import validate_url, sanitize_url

# Cargar .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

# -------- Comandos --------

# /start
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "No autorizado.")
    bot.reply_to(message, "👋 Bienvenido. Usa los comandos disponibles.")

# /nmap
@bot.message_handler(commands=['nmap'])
def nmap_scan(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")

    target = message.text.replace('/nmap', '').strip()
    if not target:
        return bot.send_message(message.chat.id, "❗ Ejemplo: `/nmap google.com`", parse_mode="Markdown")

    bot.send_message(message.chat.id, f"🔍 Escaneando `{target}` (Normal)...", parse_mode="Markdown")
    result = scan_host(target)
    file_path = save_log("nmap", result)
    bot.send_message(message.chat.id, result)
    with open(file_path, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

# /nmapfull
@bot.message_handler(commands=['nmapfull'])
def nmapfull_scan(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")

    target = message.text.replace('/nmapfull', '').strip()
    if not target:
        return bot.send_message(message.chat.id, "❗ Ejemplo: `/nmapfull google.com`", parse_mode="Markdown")

    bot.send_message(message.chat.id, f"🚀 Escaneando `{target}` (FULL)...", parse_mode="Markdown")
    result = scan_host_full(target)
    file_path = save_log("nmap_full", result)
    bot.send_message(message.chat.id, result)
    with open(file_path, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

# /nmapstealth
@bot.message_handler(commands=['nmapstealth'])
def nmapstealth_scan(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")

    target = message.text.replace('/nmapstealth', '').strip()
    if not target:
        return bot.send_message(message.chat.id, "❗ Ejemplo: `/nmapstealth google.com`", parse_mode="Markdown")

    bot.send_message(message.chat.id, f"🕵️ Escaneando `{target}` (STEALTH)...", parse_mode="Markdown")
    result = scan_host_stealth(target)
    file_path = save_log("nmap_stealth", result)
    bot.send_message(message.chat.id, result)
    with open(file_path, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

# /nmapvuln
@bot.message_handler(commands=['nmapvuln'])
def nmapvuln_scan(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")

    target = message.text.replace('/nmapvuln', '').strip()
    if not target:
        return bot.send_message(message.chat.id, "❗ Ejemplo: `/nmapvuln google.com`", parse_mode="Markdown")

    bot.send_message(message.chat.id, f"💀 Escaneando `{target}` (VULN)...", parse_mode="Markdown")
    result = scan_host_vuln(target)
    file_path = save_log("nmap_vuln", result)
    bot.send_message(message.chat.id, result)
    with open(file_path, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

# /inject
@bot.message_handler(commands=['inject'])
def inject_sql(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")

    url = message.text.replace('/inject', '').strip()
    if not validate_url(url):
        return bot.send_message(message.chat.id, "❗ Ejemplo: `/inject http://site.com?id=1`", parse_mode="Markdown")

    url = sanitize_url(url)
    bot.send_message(message.chat.id, f"💉 Inyectando en `{url}`...", parse_mode="Markdown")
    result = extract_database_name(url)
    file_path = save_log("injector", result)
    bot.send_message(message.chat.id, result)
    with open(file_path, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

# /brute
@bot.message_handler(commands=['brute'])
def brute_force(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")

    url = "http://victima.com/login.php"
    user_field = "username"
    pass_field = "password"
    success_indicator = "Bienvenido"
    user_list = "modules/wordlists/users.txt"
    pass_list = "modules/wordlists/passwords.txt"

    bot.send_message(message.chat.id, "🔐 Ejecutando fuerza bruta...")
    result = bruteforce_login(url, user_field, pass_field, success_indicator, user_list, pass_list)
    file_path = save_log("bruteforce", result)
    bot.send_message(message.chat.id, result)
    with open(file_path, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

# /scanform
@bot.message_handler(commands=['scanform'])
def scan_forms_command(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")

    url = message.text.replace('/scanform', '').strip()
    if not validate_url(url):
        return bot.send_message(message.chat.id, "❗ Ejemplo: `/scanform http://site.com`", parse_mode="Markdown")

    url = sanitize_url(url)
    bot.send_message(message.chat.id, f"🔎 Buscando formularios en `{url}`...", parse_mode="Markdown")
    result = scan_forms(url)
    file_path = save_log("formscanner", result)
    bot.send_message(message.chat.id, result)
    with open(file_path, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

# /exploit
@bot.message_handler(commands=['exploit'])
def suggest_exploit(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")

    service = message.text.replace('/exploit', '').strip()
    if not service:
        return bot.send_message(message.chat.id, "❗ Ejemplo: `/exploit apache`", parse_mode="Markdown")

    suggestion = suggest_exploits(service)
    bot.send_message(message.chat.id, f"🧠 Exploit sugerido:\n{suggestion}")

# /logs (pendiente)
@bot.message_handler(commands=['logs'])
def handle_logs(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")
    bot.send_message(message.chat.id, "📚 Pronto podrás descargar todos los logs directamente.")

# Default
@bot.message_handler(func=lambda msg: True)
def fallback(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "Acceso denegado.")
    bot.send_message(message.chat.id, "❓ Comando no reconocido. Usa `/start` para ver opciones.")

bot.infinity_polling()
