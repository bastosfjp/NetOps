import time
import requests
from rich.console import Console
from rich.table import Table

console = Console()

def run_http_check(url: str):

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    console.print(f"\n[bold cyan]HTTP Check → {url}[/bold cyan]\n")

    try:
        inicio = time.time()
        resp = requests.get(url, timeout=10, allow_redirects=True)
        tempo = round((time.time() - inicio) * 1000, 2)

        if resp.status_code < 400:
            cor_status = "bold green"
        elif resp.status_code < 500:
            cor_status = "bold yellow"
        else:
            cor_status = "bold red"

        tabela = Table("Campo", "Valor", show_header=True, header_style="bold cyan")
        tabela.add_row("Status",       f"[{cor_status}]{resp.status_code}[/{cor_status}]")
        tabela.add_row("Tempo",        f"{tempo}ms")
        tabela.add_row("URL final",    str(resp.url))
        tabela.add_row("Servidor",     resp.headers.get("Server", "não informado"))
        tabela.add_row("Content-Type", resp.headers.get("Content-Type", "não informado"))
        tabela.add_row("Tamanho",      f"{len(resp.content)} bytes")

        console.print(tabela)

    except requests.exceptions.ConnectionError:
        console.print(f"[bold red]✗ Não foi possível conectar em {url}[/bold red]")
    except requests.exceptions.Timeout:
        console.print("[bold red]✗ Timeout — servidor demorou demais para responder[/bold red]")
    except requests.exceptions.InvalidURL:
        console.print("[bold red]✗ URL inválida[/bold red]")
    except Exception as e:
        console.print(f"[bold red]✗ Erro inesperado: {e}[/bold red]")