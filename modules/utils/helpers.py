# utils/helpers.py

import socket
import re
from urllib.parse import urlparse

def validate_url(url):
    """Valida si la URL tiene un formato correcto."""
    regex = re.compile(
        r'^(http|https)://'  # debe empezar por http o https
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6})'  # dominio
        r'(:\d+)?'  # puerto opcional
        r'(/.*)?$'  # path opcional
    )
    return re.match(regex, url) is not None

def resolve_ip(hostname):
    """Resuelve un hostname a una dirección IP."""
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        return None

def get_domain(url):
    """Extrae el dominio de una URL."""
    parsed = urlparse(url)
    return parsed.netloc

def sanitize_url(url):
    """Elimina caracteres sospechosos para evitar problemas."""
    return url.replace("'", "").replace('"', "").replace(";", "").replace("--", "")

def prepare_payloads(base_payloads):
    """Genera combinaciones de payloads para fuzzing."""
    payloads = []
    wrappers = ["'", '"', "`", "(", ")"]
    for base in base_payloads:
        for wrap in wrappers:
            payloads.append(f"{wrap}{base}{wrap}")
    return list(set(payloads))  # Evitar duplicados
