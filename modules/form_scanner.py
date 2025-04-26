# modules/form_scanner.py

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (PentestingBot)"
}

def scan_forms(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            return f"❗ Error al acceder al sitio: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        if not forms:
            return "⚠️ No se detectaron formularios en esta página."

        results = []
        for idx, form in enumerate(forms, 1):
            action = form.get("action", "N/A")
            method = form.get("method", "GET").upper()
            inputs = []
            for input_tag in form.find_all("input"):
                input_type = input_tag.get("type", "text")
                input_name = input_tag.get("name", "N/A")
                inputs.append(f"{input_name} ({input_type})")
            form_info = f"📝 Formulario #{idx}\n🔗 Acción: {action}\n🚀 Método: {method}\n📥 Inputs: {', '.join(inputs)}"
            results.append(form_info)

        return "\n\n".join(results)

    except Exception as e:
        return f"❌ Error escaneando formularios: {str(e)}"
