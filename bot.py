import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import telebot
from dotenv import load_dotenv

# Importar módulos propios
from modules.sqli_scanner import scan_url
from modules.nmap_scanner import scan_host, scan_host_full, scan_host_stealth, scan_host_vuln
from modules.injector import extract_database_name
from modules.bruteforcer import bruteforce_login
from modules.form_scanner import scan_forms
from modules.logger import save_log
from modules.exploit_suggester import suggest_exploits
from modules.utils.helpers import validate_url, sanitize_url

# Cargar variables de entorno
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

bot = telebot.TeleBot(BOT_TOKEN)

def is_authorized(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "🚫 No autorizado.")
        return False
    return True

# Comando: /start
@bot.message_handler(commands=['start'])
def start(message):
    if not is_authorized(message): return
    bot.reply_to(message, "👋 Bienvenido. Usa los comandos disponibles.")

# Comando: /nmap
@bot.message_handler(commands=['nmap'])
def nmap_scan(message):
    if not is_authorized(message): return
    target = message.text.replace('/nmap', '').strip()
    if not target:
        return bot.send_message(message.chat.id, "❗ Usa: `/nmap dominio.com`", parse_mode="Markdown")

    bot.send_message(message.chat.id, f"🔍 Escaneando `{target}` (Normal)...", parse_mode="Markdown")
    result = scan_host(target)
    send_result(message.chat.id, result, "nmap")

# Comando: /nmapfull
@bot.message_handler(commands=['nmapfull'])
def nmapfull_scan(message):
    if not is_authorized(message): return
    target = message.text.replace('/nmapfull', '').strip()
    if not target:
        return bot.send_message(message.chat.id, "❗ Usa: `/nmapfull dominio.com`", parse_mode="Markdown")

    bot.send_message(message.chat.id, f"🚀 Escaneando `{target}` (FULL)...", parse_mode="Markdown")
    result = scan_host_full(target)
    send_result(message.chat.id, result, "nmap_full")

# Comando: /nmapstealth
@bot.message_handler(commands=['nmapstealth'])
def nmapstealth_scan(message):
    if not is_authorized(message): return
    target = message.text.replace('/nmapstealth', '').strip()
    if not target:
        return bot.send_message(message.chat.id, "❗ Usa: `/nmapstealth dominio.com`", parse_mode="Markdown")

    bot.send_message(message.chat.id, f"🕵️ Escaneando `{target}` (Stealth)...", parse_mode="Markdown")
    result = scan_host_stealth(target)
    send_result(message.chat.id, result, "nmap_stealth")

# Comando: /nmapvuln
@bot.message_handler(commands=['nmapvuln'])
def nmapvuln_scan(message):
    if not is_authorized(message): return
    target = message.text.replace('/nmapvuln', '').strip()
    if not target:
        return bot.send_message(message.chat.id, "❗ Usa: `/nmapvuln dominio.com`", parse_mode="Markdown")

    bot.send_message(message.chat.id, f"💀 Escaneando `{target}` (Vulnerabilidades)...", parse_mode="Markdown")
    result = scan_host_vuln(target)
    send_result(message.chat.id, result, "nmap_vuln")

# Comando: /inject
@bot.message_handler(commands=['inject'])
def inject_sql(message):
    if not is_authorized(message): return
    url = message.text.replace('/inject', '').strip()
    if not validate_url(url):
        return bot.send_message(message.chat.id, "❗ Usa: `/inject http://sitio.com?id=1`", parse_mode="Markdown")

    url = sanitize_url(url)
    bot.send_message(message.chat.id, f"💉 Inyectando en `{url}`...", parse_mode="Markdown")
    result = extract_database_name(url)
    send_result(message.chat.id, result, "injector")

# Comando: /brute
@bot.message_handler(commands=['brute'])
def brute_force(message):
    if not is_authorized(message): return

    url = "http://victima.com/login.php"
    user_field = "username"
    pass_field = "password"
    success_indicator = "Bienvenido"
    user_list = "modules/wordlists/users.txt"
    pass_list = "modules/wordlists/passwords.txt"

    bot.send_message(message.chat.id, "🔐 Ejecutando ataque de fuerza bruta...")
    result = bruteforce_login(url, user_field, pass_field, success_indicator, user_list, pass_list)
    send_result(message.chat.id, result, "bruteforce")

# Comando: /scanform
@bot.message_handler(commands=['scanform'])
def scan_forms_command(message):
    if not is_authorized(message): return
    url = message.text.replace('/scanform', '').strip()
    if not validate_url(url):
        return bot.send_message(message.chat.id, "❗ Usa: `/scanform http://sitio.com`", parse_mode="Markdown")

    url = sanitize_url(url)
    bot.send_message(message.chat.id, f"🔎 Buscando formularios en `{url}`...", parse_mode="Markdown")
    result = scan_forms(url)
    send_result(message.chat.id, result, "formscanner")

# Comando: /exploit
@bot.message_handler(commands=['exploit'])
def suggest_exploit(message):
    if not is_authorized(message): return
    service = message.text.replace('/exploit', '').strip()
    if not service:
        return bot.send_message(message.chat.id, "❗ Usa: `/exploit apache`", parse_mode="Markdown")

    suggestion = suggest_exploits(service)
    bot.send_message(message.chat.id, f"🧠 Exploit sugerido:\n{suggestion}")

# Comando: /logs
@bot.message_handler(commands=['logs'])
def handle_logs(message):
    if not is_authorized(message): return
    bot.send_message(message.chat.id, "📚 Pronto podrás descargar todos los logs directamente.")

# Mensajes que no son comandos
@bot.message_handler(func=lambda message: True)
def fallback(message):
    if not is_authorized(message): return
    bot.send_message(message.chat.id, "❓ Comando no reconocido. Usa `/start` para ver opciones.")

# Función para enviar resultados y logs
def send_result(chat_id, result, module_name):
    file_path = save_log(module_name, result)
    bot.send_message(chat_id, result)
    with open(file_path, 'rb') as file:
        bot.send_document(chat_id, file)

# Ejecutar el bot
if __name__ == "__main__":
    bot.infinity_polling()
