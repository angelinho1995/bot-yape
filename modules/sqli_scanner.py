# modules/sqli_scanner.py

import requests

def scan_url(url):
    try:
        payloads = ["' OR '1'='1", "' OR 1=1 --", "' OR '1'='1' --"]
        vulnerable = False

        for payload in payloads:
            test_url = url + payload
            response = requests.get(test_url)

            if any(error in response.text.lower() for error in ["sql", "syntax", "warning", "mysql", "query"]):
                vulnerable = True
                return f"🚨 Vulnerabilidad detectada con payload: {payload}"

        return "✅ No se detectó SQLi con payloads simples."
    except Exception as e:
        return f"⚠️ Error al escanear: {str(e)}"
