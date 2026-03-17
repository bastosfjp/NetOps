import subprocess
import sys
from rich.console import Console

console = Console()

def run_tracert(host:str):
    console.print(f"\n[bold cyan]Traceroute → {host}[bold cyan]\n")

    # windows usa tracert mac e linux usam traceroute
    comando = "tracert" if sys.platform == "win32" else "traceroute"

    if ":" in host:
        tipo_ip = "-6"
    elif all(c.isdigit or c == "." for c in host):
        tipo_ip = "-4"
    else:
        tipo_ip = ""

    try:
        processo = subprocess.Popen(
            [comando,tipo_ip,host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    # imprime linha por linha conforme vai chegando
        for linha in processo.stdout:
            linha = linha.rstrip()
            if linha:
                console.print(linha)

        processo.wait()
        
        if processo.returncode != 0:
            console.print(f"\n[bold red]✗ Traceroute falhou para {host}[/bold red]")

    except FileNotFoundError:
        console.print(f"[red]✗ Comando '{comando}' não encontrado no sistema[/red]")
    except Exception as e:
        console.print(f"\n[bold red]✗ Erro inesperado: {e}[/bold red]")