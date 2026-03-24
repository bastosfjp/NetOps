import subprocess
import sys
import threading
import time
import socket
from dataclasses import dataclass, field
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich import box

console = Console()


@dataclass
class HopStats:
    indice:   int
    host:     str
    enviados: int = 0
    perdidos: int = 0
    latencias: list = field(default_factory=list)

    @property
    def perda(self) -> float:
        if self.enviados == 0:
            return 0.0
        return round((self.perdidos / self.enviados) * 100, 1)

    @property
    def avg(self) -> str:
        if not self.latencias:
            return "—"
        return f"{round(sum(self.latencias) / len(self.latencias))}ms"

    @property
    def minimo(self) -> str:
        if not self.latencias:
            return "—"
        return f"{min(self.latencias)}ms"

    @property
    def maximo(self) -> str:
        if not self.latencias:
            return "—"
        return f"{max(self.latencias)}ms"


# --- descoberta de hops ---

def descobrir_hops(host: str) -> list[str]:
    console.print(f"\n[dim]Mapeando rota para {host}...[/dim]")

    comando = ["tracert", "-d", "-h", "20", host] if sys.platform == "win32" \
              else ["traceroute", "-n", "-m", "20", host]

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding="cp850" if sys.platform == "win32" else "utf-8",
            timeout=30
        )

        hops = []
        for linha in resultado.stdout.splitlines():
            partes = linha.split()
            for parte in partes:
                try:
                    socket.inet_aton(parte)   # verifica se é um IP válido
                    if parte not in ["0.0.0.0", "255.255.255.255"]:
                        hops.append(parte)
                        break
                except socket.error:
                    continue

        return hops

    except Exception as e:
        console.print(f"[bold red]✗ Erro ao mapear rota: {e}[/bold red]")
        return []


# --- ping de um hop ---

def pingar_hop(hop: HopStats, parar: threading.Event):
    flag     = "-n" if sys.platform == "win32" else "-c"
    encoding = "cp850" if sys.platform == "win32" else "utf-8"

    while not parar.is_set():
        hop.enviados += 1
        try:
            inicio    = time.time()
            resultado = subprocess.run(
                ["ping", flag, "1", "-w", "1000", hop.host],
                capture_output=True,
                text=True,
                encoding=encoding,
                timeout=2
            )
            tempo = round((time.time() - inicio) * 1000)

            if resultado.returncode == 0:
                hop.latencias.append(tempo)
            else:
                hop.perdidos += 1

        except Exception:
            hop.perdidos += 1

        time.sleep(1)


# --- tabela de exibição ---

def montar_tabela(hops: list[HopStats], ciclos: int) -> Table:
    tabela = Table(
        "#", "Host", "Loss%", "Enviados", "Mín", "Méd", "Máx",
        box=box.SIMPLE,
        header_style="bold cyan",
        padding=(0, 1),
        show_edge=False
    )

    for hop in hops:
        # cor da perda
        if hop.perda == 0:
            perda_txt = Text(f"{hop.perda}%", style="green")
        elif hop.perda < 10:
            perda_txt = Text(f"{hop.perda}%", style="yellow")
        else:
            perda_txt = Text(f"{hop.perda}%", style="bold red")

        tabela.add_row(
            str(hop.indice),
            hop.host,
            perda_txt,
            str(hop.enviados),
            hop.minimo,
            hop.avg,
            hop.maximo
        )

    return tabela


# --- entry point ---

def run_monitor(host: str):
    console.print(f"\n[bold cyan]Monitor MTR → {host}[/bold cyan]")

    hops_ips = descobrir_hops(host)

    if not hops_ips:
        console.print("[bold red]✗ Não foi possível mapear a rota.[/bold red]")
        return "Não foi possível mapear a rota"

    # cria objeto HopStats pra cada hop
    hops = [HopStats(indice=i+1, host=ip) for i, ip in enumerate(hops_ips)]

    # evento pra sinalizar as threads pararem
    parar = threading.Event()

    # inicia uma thread de ping pra cada hop
    threads = []
    for hop in hops:
        t = threading.Thread(target=pingar_hop, args=(hop, parar), daemon=True)
        t.start()
        threads.append(t)

    console.print("[dim]Monitorando... pressione Ctrl+C para parar[/dim]\n")

    ciclos = 0
    try:
        with Live(console=console, refresh_per_second=1) as live:
            while True:
                ciclos += 1
                tabela = montar_tabela(hops, ciclos)
                live.update(tabela)
                time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        parar.set()
        for t in threads:
            t.join(timeout=2)

    console.print("\n[dim]Monitor encerrado.[/dim]")

    return {
        "hops": [
            {
                "indice":   h.indice,
                "host":     h.host,
                "perda":    f"{h.perda}%",
                "avg":      h.avg,
                "min":      h.minimo,
                "max":      h.maximo,
                "enviados": h.enviados
            }
            for h in hops
        ]
    }