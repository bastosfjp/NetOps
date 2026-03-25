from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()

# --- banner ---

def exibir_banner():
    console.print("""
[bold cyan]
 ███╗   ██╗███████╗████████╗ ██████╗ ██████╗ ███████╗
 ████╗  ██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝
 ██╔██╗ ██║█████╗     ██║   ██║   ██║██████╔╝███████╗
 ██║╚██╗██║██╔══╝     ██║   ██║   ██║██╔═══╝ ╚════██║
 ██║ ╚████║███████╗   ██║   ╚██████╔╝██║     ███████║
 ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ╚══════╝
[/bold cyan]
[dim]  canivete suíço de redes — by @bastosfjp[/dim]
""")

# --- pegar informações ---

def pedir_host(ferramenta: str) -> str:
    return console.input(f"\n[cyan]{ferramenta}[/cyan] → host/IP: ").strip()

def pedir_url() -> str:
    return console.input("\n[cyan]http[/cyan] → URL: ").strip()

def opcao_invalida():
    console.print("[red]Opção inválida.[/red] Tente novamente.")

def voltar():
    console.input("\n[dim]Enter para voltar...[/dim]")


# --- painel de informação do sistema ---

def exibir_sysinfo():
    from utils.sysinfo import coletar_tudo

    console.print(Align("[dim]coletando informações do sistema...[/dim]", align="center"))
    
    info = coletar_tudo()
    pub = info["ip_publico"]

    localidade = f"{pub['cidade']}, {pub['regiao']} — {pub['pais']}" \
                 if pub["cidade"] else pub["pais"]

    texto = Text(justify="center")
    texto.append(f"  v{info['versao']}", style="bold cyan")
    texto.append("   |   ")
    texto.append(f"{info['datetime']}", style="bold")
    texto.append("\n\n")

    texto.append("  Hostname  ", style="dim")
    texto.append(f"{info['hostname']}\n", style="bold")

    texto.append("  IP local  ", style="dim")
    texto.append(f"{info['ip_local']}\n", style="bold")

    texto.append("  IP público  ", style="dim")
    texto.append(f"{pub['ip']}", style="bold cyan")
    texto.append(f"  {localidade}\n", style="dim")

    texto.append("  Provedor  ", style="dim")
    texto.append(f"{pub['provedor']}", style="bold")

    console.print(Panel(texto, box=box.ROUNDED, border_style="cyan"))


# --- submenus ---

def menu_conectividade():
    from tools.ping import run_ping
    from tools.tracert import run_tracert
    from utils.reporter import perguntar_salvar
    from utils.historico import registrar

    while True:
        console.print()
        texto = Text()
        texto.append("  1. ", style="bold cyan"); texto.append("Ping\n")
        texto.append("  2. ", style="bold cyan"); texto.append("Traceroute\n")
        texto.append("  0. ", style="bold red");  texto.append("Voltar")
        console.print(Panel(texto, title="[bold]Conectividade[/bold]", width=45))

        escolha = console.input("\nEscolha: ").strip()

        if escolha == "0":
            break
        elif escolha == "1":
            host = pedir_host("ping")
            output = run_ping(host)
            status = "timeout" if "timeout" in str(output).lower() else "erro" if "erro" in str(output).lower() else "sucesso"                                     # ← linha nova
            registrar("ping", host, status) 
            perguntar_salvar("ping", host,{"output":output})
            voltar()
        elif escolha == "2":
            host   = pedir_host("tracert")
            output = None               
            output = run_tracert(host)
            status = "timeout" if "timeout" in str(output).lower() \
                    else "erro" if output is None or "erro" in str(output).lower() \
                    else "sucesso"
            registrar("tracert", host, status)
            perguntar_salvar("tracert", host, {"output": output})
            voltar()
        else:
            opcao_invalida()


def menu_diagnostico():
    from tools.portscan import run_portscan
    from utils.reporter import perguntar_salvar
    from utils.historico import registrar

    while True:
        console.print()
        texto = Text()
        texto.append("  1. ", style="bold cyan"); texto.append("Port Scanner\n")
        texto.append("  0. ", style="bold red");  texto.append("Voltar")
        console.print(Panel(texto, title="[bold]Diagnóstico[/bold]", width=45))

        escolha = console.input("\nEscolha: ").strip()

        if escolha == "0":
            break
        elif escolha == "1":
            host = pedir_host("scan")
            output = run_portscan(host)
            status = "timeout" if "timeout" in str(output).lower() else "erro" if "erro" in str(output).lower() else "sucesso"                                     # ← linha nova
            registrar("portscan", host, status)
            perguntar_salvar("scan", host, output if isinstance(output, dict) else {"output": output})
            voltar()
        elif escolha == "2":
            console.print("[dim]Em breve...[/dim]")
        else:
            opcao_invalida()


def menu_servicos_web():
    from tools.dns import run_dns
    from tools.http_check import run_http_check
    from tools.ssl_check import run_ssl_check
    from utils.reporter import perguntar_salvar
    from utils.historico import registrar

    while True:
        console.print()
        texto = Text()
        texto.append("  1. ", style="bold cyan"); texto.append("DNS Lookup\n")
        texto.append("  2. ", style="bold cyan"); texto.append("HTTP Check\n")
        texto.append("  3. ", style="bold cyan"); texto.append("SSL Check\n")
        texto.append("  0. ", style="bold red");  texto.append("Voltar")
        console.print(Panel(texto, title="[bold]Serviços Web[/bold]", width=45))

        escolha = console.input("\nEscolha: ").strip()

        if escolha == "0":
            break
        elif escolha == "1":
            host = pedir_host("dns")
            output = run_dns(host)
            status = "timeout" if "timeout" in str(output).lower() else "erro" if "erro" in str(output).lower() else "sucesso"                                     # ← linha nova
            registrar("dns", host, status)
            perguntar_salvar("dns", host, {"output": output})
            voltar()
        elif escolha == "2":
            url = pedir_url()
            output = run_http_check(url)
            status = "timeout" if "timeout" in str(output).lower() else "erro" if "erro" in str(output).lower() else "sucesso"                                     # ← linha nova
            registrar("http", host, status)
            perguntar_salvar("http", url, output if isinstance(output, dict) else {"output": output})
            voltar()
        elif escolha == "3":
            host = pedir_host("ssl")
            output = run_ssl_check(host)
            status = "timeout" if "timeout" in str(output).lower() else "erro" if "erro" in str(output).lower() else "sucesso"                                     # ← linha nova
            registrar("ssl", host, status)
            perguntar_salvar("ssl", host, output if isinstance(output, dict) else {"output": output})
            voltar()
        else:
            opcao_invalida()


def menu_monitor():
    from tools.monitor import run_monitor
    from utils.historico import registrar
    from utils.reporter import perguntar_salvar

    while True:
        console.print()
        texto = Text()
        texto.append("  1. ", style="bold cyan"); texto.append("Monitor MTR\n")
        texto.append("  0. ", style="bold red");  texto.append("Voltar")
        console.print(Panel(texto, title="[bold]Monitor[/bold]", width=45))

        escolha = console.input("\nEscolha: ").strip()

        if escolha == "0":
            break
        elif escolha == "1":
            host   = pedir_host("monitor")
            output = run_monitor(host)
            status = "erro" if isinstance(output, str) else "sucesso"
            registrar("monitor", host, status)
            perguntar_salvar("monitor", host, output if isinstance(output, dict) else {"output": output})
            voltar()
        else:
            opcao_invalida()

# --- menu principal ---

def exibir_menu_principal():
    texto = Text()
    texto.append("  ── ferramentas ──────────────────\n", style="dim")
    texto.append("  1. ", style="bold cyan");   texto.append("Conectividade\n")
    texto.append("  2. ", style="bold cyan");   texto.append("Diagnóstico\n")
    texto.append("  3. ", style="bold cyan");   texto.append("Serviços Web\n")
    texto.append("  4. ", style="bold cyan");   texto.append("Monitor\n")
    texto.append("\n")
    texto.append("  ── utilitários ──────────────────\n", style="dim")
    texto.append("  5. ", style="bold cyan"); texto.append("Relatórios\n")
    texto.append("  6. ", style="bold cyan"); texto.append("Histórico\n")
    texto.append("\n")
    texto.append("  0. ", style="bold red");    texto.append("Sair")

    console.print(Panel(
        texto,
        title="[bold cyan]NetOps[/bold cyan]",
        subtitle="[dim]canivete suíço de redes[/dim]",
        box=box.ROUNDED,
        border_style="cyan",
        width=48
    ))

def run_menu():
    console.clear()
    exibir_banner()
    exibir_sysinfo()

    from utils.relatorios import run_relatorios
    from utils.historico import run_historico


    while True:
        console.print()
        exibir_menu_principal()
        escolha = console.input("\nEscolha uma área: ").strip()

        if escolha == "0":
            console.print("\n[bold]Até mais![/bold]\n")
            break
        elif escolha == "1":
            menu_conectividade()
        elif escolha == "2":
            menu_diagnostico()
        elif escolha == "3":
            menu_servicos_web()
        elif escolha == "4":
            menu_monitor()
        elif escolha == "5":
            run_relatorios()
        elif escolha == "6":
            run_historico()
        else:
            opcao_invalida()
