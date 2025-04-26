# modules/nmap_scanner.py

import nmap
from urllib.parse import urlparse

def limpiar_target(raw_input):
    """Extrae dominio o IP desde una URL o texto directo."""
    try:
        parsed = urlparse(raw_input)
        if parsed.netloc:
            return parsed.netloc
        elif parsed.path:
            return parsed.path.split("/")[0]
        else:
            return raw_input.strip()
    except Exception:
        return raw_input.strip()

def ejecutar_scan(raw_input, arguments):
    """Función general que ejecuta el escaneo con argumentos personalizados de Nmap."""
    nm = nmap.PortScanner()
    result = []

    # Limpiar el objetivo (dominio o IP)
    target = limpiar_target(raw_input)

    try:
        nm.scan(hosts=target, arguments=arguments)

        if target not in nm.all_hosts():
            return "❌ El objetivo no respondió o es inválido."

        # Resultado básico
        result.append(f"📍 Objetivo: {target}")
        result.append(f"🛠️ Argumentos usados: `{arguments}`")

        # Detallar puertos y servicios
        for proto in nm[target].all_protocols():
            ports = nm[target][proto].keys()
            for port in sorted(ports):
                service = nm[target][proto][port]
                name = service.get('name', 'desconocido')
                version = service.get('version', 'N/A')
                product = service.get('product', 'N/A')
                extrainfo = service.get('extrainfo', '')
                state = service.get('state', 'unknown')
                banner = f"{product} {version}".strip()
                extra = f" ({extrainfo})" if extrainfo else ""

                result.append(f"🟢 {port}/{proto} [{state}] - {name} → {banner}{extra}")

        return "\n".join(result) if result else "⚠️ No se detectaron puertos abiertos."

    except Exception as e:
        return f"❗ Error durante el escaneo Nmap: {str(e)}"

# Funciones específicas de tipo de escaneo

def scan_host(raw_target):
    """Escaneo estándar (detección de versiones, OS, scripts básicos)."""
    return ejecutar_scan(raw_target, "-T4 -sV -sC -A -Pn")

def scan_host_full(raw_target):
    """Escaneo completo, detallado y agresivo."""
    return ejecutar_scan(raw_target, "-T5 -sS -sV -sC -O -A -Pn")

def scan_host_stealth(raw_target):
    """Escaneo sigiloso para evadir firewalls."""
    return ejecutar_scan(raw_target, "-T2 -sS -Pn -f")

def scan_host_vuln(raw_target):
    """Escaneo orientado a encontrar vulnerabilidades conocidas."""
    return ejecutar_scan(raw_target, "-sV --script vuln -Pn")
