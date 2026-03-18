import socket
import datetime
import requests

VERSAO = "0.1.0"

def get_hostname():
    try:
        return socket.gethostname()
    except Exception:
        return "desconhecido"
    
def get_ip_local():
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "desconhecido"
    
def get_ip_publico():
    try:
        resp = requests.get("https://ipinfo.io/json", timeout=5)
        dados = resp.json()
        return {
            "ip":       dados.get("ip", "desconhecido"),
            "provedor": dados.get("org", "desconhecido"),
            "cidade":   dados.get("city", ""),
            "regiao":   dados.get("region", ""),
            "pais":     dados.get("country", "")
        }
    except Exception:
        return {
            "ip":       "sem conexão",
            "provedor": "sem conexão",
            "cidade":   "",
            "regiao":   "",
            "pais":     ""
        }
def get_datetime():
    agora = datetime.datetime.now()
    return agora.strftime("%d/%m/%Y  %H:%M:%S")

def coletar_tudo():
    return {
        "versao":    VERSAO,
        "datetime":  get_datetime(),
        "hostname":  get_hostname(),
        "ip_local":  get_ip_local(),
        "ip_publico": get_ip_publico()
    }