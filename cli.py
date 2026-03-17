from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# utils
from tools.ping import run_ping
from tools.tracert import run_tracert
from tools.portscan import run_portscan
from tools.dns import run_dns
from tools.http_check import run_http_check

console = Console()

def exibir_menu():
    texto = Text()

    texto.append(" 1. ", style="bold cyan")
    texto.append("Ping\n")
    texto.append(" 2. ", style="bold cyan")
    texto.append("Traceroute\n")
    texto.append(" 3. ", style="bold cyan")
    texto.append("Port Scanner\n")
    texto.append(" 4. ", style="bold cyan")
    texto.append("DNS Lookup\n")
    texto.append(" 5. ", style="bold cyan")
    texto.append("HTTP Check\n")
    texto.append(" 0. ", style="bold red")
    texto.append("SAIR\n")

    console.print(Panel(texto, title="[bold] NetSuite [/bold]", subtitle="canivete suíço de redes", width=45))

def pedir_host(ferramenta:str) -> str:
    return console.input(f"[cyan]{ferramenta}[/cyan] → host/IP: ").strip()

def pedir_url() -> str:
    return console.input("[cyan]http[/cyan] → URL: ").strip()

def run_menu():
    while True:
        console.print()
        exibir_menu()
        escolha = console.input("\nEscolha uma opção: ").strip()

        if escolha == "0":
            console.print("\n[yellow bold]Até mais![/yellow bold]\n")
            break
        elif escolha == "1":
            host = pedir_host("ping")
            run_ping(host)
        elif escolha == "2":
            host = pedir_host("traceroute")
            run_tracert(host)
        elif escolha == "3":
            host = pedir_host("scan")
            run_portscan(host)
        elif escolha == "4":
            host = pedir_host("dns")
            run_dns(host)
        elif escolha == "5":
            url = pedir_url()
            run_http_check(url)
        else:
            console.print("[red]Opção inválida.[/red] Tente novamente.")
