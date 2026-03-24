import subprocess
import sys
from rich.console import Console

console = Console()

def run_ping(host:str):
    console.print(f"\n [bold cyan]Ping → {host}[/bold cyan]")

    # Windows usa -n, Linux/Mac usa -c pra definir quantidade de pacotes

    flag = "-n" if sys.platform == "win32" else "-c"

    # coleta e valida inputs primeiro
    tipo_ip = console.input("Informe o tipo de IP: IPv6 [6] ou IPv4 [4]: ").strip()
    if tipo_ip not in ["4", "6"]:
        console.print("\n[bold red]✗ Digite apenas 4 ou 6[/bold red]")
        return

    pacotes = console.input(f"Informe a quantidade de pacotes no [bold cyan]ping[/bold cyan]: ").strip()
    if not pacotes.isdigit():
        console.print("\n[bold red]✗ Digite apenas números inteiros[/bold red]")
        return
    
    console.print()

    try:
        resultado = subprocess.run(
            ["ping","-"+ tipo_ip, flag, pacotes,host],
            capture_output=True,
            text=True,
            encoding="cp850",
            timeout=15
        )

        if resultado.returncode == 0:
            console.print(resultado.stdout)
            return resultado.stdout
        else:
            console.print(f"\n[bold red]✗ Host {host} não respondeu[/bold red]")
            return f"Host {host} não respondeu"

    except subprocess.TimeoutExpired:
        console.print("\n[bold red]✗ Timeout — host demorou demais[/bold red]")
        return "Timeout"
    except Exception as e:
        console.print(f"\n[bold red]✗ Erro inesperado: {e}[/bold red]")
        return f"Erro: {e}"
