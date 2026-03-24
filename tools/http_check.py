import time
import requests
from rich.console import Console
from rich.table import Table

console = Console()

def run_http_check(url: str):
    if not url.startswith("http"):
        url = "https://" + url

    console.print(f"\n[bold cyan]HTTP Check → {url}[/bold cyan]\n")

    try:
        inicio = time.time()
        resp   = requests.get(url, timeout=10, allow_redirects=True)
        tempo  = round((time.time() - inicio) * 1000, 2)

        console.print(f"[green]✓[/green] Status: [bold]{resp.status_code}[/bold] em {tempo}ms")
        console.print(f"[cyan]→[/cyan] Content-Type: {resp.headers.get('Content-Type', 'N/A')}")
        console.print(f"[cyan]→[/cyan] Servidor: {resp.headers.get('Server', 'N/A')}")

        return {                                     # ← devolve dicionário
            "status":       resp.status_code,
            "tempo_ms":     tempo,
            "content_type": resp.headers.get("Content-Type", "N/A"),
            "servidor":     resp.headers.get("Server", "N/A"),
            "url_final":    resp.url
        }

    except requests.exceptions.ConnectionError:
        console.print("[bold red]✗ Não foi possível conectar[/bold red]")
        return "Não foi possível conectar"
    except requests.exceptions.Timeout:
        console.print("[bold red]✗ Timeout[/bold red]")
        return "Timeout"
    except Exception as e:
        console.print(f"[bold red]✗ Erro: {e}[/bold red]")
        return f"Erro: {e}"