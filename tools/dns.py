import dns.resolver
from rich.console import Console
from rich.table import Table

console = Console()

TIPOS_REGISTRO = {
    "A":     "Endereço IPv4",
    "AAAA":  "Endereço IPv6",
    "MX":    "Servidor de e-mail",
    "NS":    "Servidores DNS autoritativos",
    "TXT":   "Verificações e políticas (SPF, DKIM...)",
    "CNAME": "Apelido para outro domínio"
}

def run_dns(host:str):
    console.print(f"\n[bold cyan]DNS Lookup → {host}[/bold cyan]\n")

    tabela = Table("Tipo","Descrição", "Valor", "TTL", show_header=True, header_style="bold cyan")
    
    encontrou = False 

    for tipo,descricao in TIPOS_REGISTRO.items():
        try:
            respostas = dns.resolver.resolve(host,tipo)
            for registro in respostas:
                tabela.add_row(
                    f"[bold]{tipo}[/bold]",
                    f"[dim]{descricao}[/dim]",
                    str(registro),
                    str(respostas.ttl)
                )
                encontrou = True
        except dns.resolver.NoAnswer:
            pass  # esse tipo não existe pra esse domínio, segue
        except dns.resolver.NXDOMAIN:
            console.print(f"[bold red]✗ Domínio {host} não existe[/bold red]")
            return
        except dns.resolver.Timeout:
            console.print(f"[yellow]⚠ Timeout ao consultar registro {tipo}[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ Erro em {tipo}: {e}[/red]")
    
    if encontrou:
        console.print(tabela)
    else:
        console.print(f"[yellow]⚠ Nenhum registro encontrado para {host}[/yellow]")
