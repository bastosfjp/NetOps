import subprocess
import sys
from rich.console import Console

console = Console()

def run_tracert(host: str):
    console.print(f"\n[bold cyan]Traceroute → {host}[/bold cyan]\n")
    comando = "tracert" if sys.platform == "win32" else "traceroute"

    try:
        processo = subprocess.Popen(
            [comando, host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="cp850",
            text=True
        )

        linhas = []
        for linha in processo.stdout:
            linha = linha.rstrip()
            if linha:
                console.print(linha)
                linhas.append(linha)    

        processo.wait()

        if processo.returncode != 0:
            console.print(f"\n[bold red]✗ Traceroute falhou para {host}[/bold red]")
            return f"Traceroute falhou para {host}"

        return "\n".join(linhas)        

    except FileNotFoundError:
        console.print(f"[red]✗ Comando '{comando}' não encontrado[/red]")
        return f"Comando {comando} não encontrado"
    except Exception as e:
        console.print(f"\n[bold red]✗ Erro inesperado: {e}[/bold red]")
        return f"Erro: {e}"