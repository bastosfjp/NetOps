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

def run_portscan(host:str):
    console.print(f"\n[bold cyan]Port Scan → {host}[/bold cyan]\n")

    try:
        ip = socket.gethostbyname(host)
        console.print(f"[cyan]→[/cyan] IP resolvido: [bold]{ip}[/bold]\n")
    except socket.gaierror:
        console.print(f"[bold red]x Não foi possível resolver o host {host}[/bold red]")
        return
    
    usar_padrao = console.input("Escanear portas padrão? [[bold]S[/bold]/N]: ").strip().lower()

    if usar_padrao in ["","s"]:
        portas = PORTAS_COMUNS
    else:
        entrada = console.input("Digite as portas separadas por vírgula (ex: 80, 443, 8080): ").strip()
        portas = {}
        for item in entrada.split(","):
            if item.isdigit() and 1 <= int(item) <= 65535:
                portas[int(item)] = "customizada"
            else:
                console.print(f"[yellow]⚠ '{item}' ignorado — porta inválida[/yellow]")

    if not portas:
        console.print("[bold red]✗ Nenhuma porta válida informada[/bold red]")
        return
    
    tabela = Table("Porta","Serviço","Status", show_header=True, header_style="bold cyan")

    abertas = 0

    for porta,servico in portas.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        resultado = sock.connect_ex((ip,porta))
        sock.close()

        if resultado == 0:
            tabela.add_row(str(porta),servico,"[bold green]aberta[/bold green]")
            abertas += 1
        else:
            tabela.add_row(str(porta),servico,"[dim]fechada[/dim]")
        
    console.print(tabela)
    console.print(f"\n[cyan]→[/cyan] {abertas} porta(s) aberta(s) de {len(portas)} verificadas")