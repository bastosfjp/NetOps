import socket
from rich.console import Console
from rich.table import Table

console = Console()

PORTAS_COMUNS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017:"MongoDB"
}

def run_portscan(host: str):
    console.print(f"\n[bold cyan]Port Scan → {host}[/bold cyan]\n")

    try:
        ip = socket.gethostbyname(host)
        console.print(f"[cyan]→[/cyan] IP resolvido: [bold]{ip}[/bold]\n")
    except socket.gaierror:
        console.print(f"[bold red]✗ Não foi possível resolver {host}[/bold red]")
        return f"Não foi possível resolver {host}"

    customizado = console.input(
        "Portas customizadas? Digite separado por vírgula ou Enter para padrão: "
    ).strip()

    if customizado:
        portas_scan = {}
        for p in customizado.split(","):
            p = p.strip()
            if p.isdigit():
                portas_scan[int(p)] = "customizada"
            else:
                console.print(f"[yellow]⚠ '{p}' ignorado — não é um número válido[/yellow]")
    else:
        portas_scan = PORTAS_COMUNS

    tabela = Table("Porta", "Serviço", "Status", show_header=True, header_style="bold cyan")

    abertas = []
    for porta, servico in portas_scan.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        resultado = sock.connect_ex((ip, porta))
        sock.close()

        if resultado == 0:
            tabela.add_row(str(porta), servico, "[bold green]aberta[/bold green]")
            abertas.append(f"{porta}/{servico}")
        else:
            tabela.add_row(str(porta), servico, "[dim]fechada[/dim]")

    console.print(tabela)
    console.print(f"\n[cyan]→[/cyan] {len(abertas)} porta(s) aberta(s) de {len(portas_scan)} verificadas")

    return {
        "ip": ip,
        "portas_abertas": abertas,
        "total_verificadas": len(portas_scan)
    }