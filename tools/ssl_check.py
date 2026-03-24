import ssl
import socket
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

def run_ssl_check(host: str):
    host = host.replace("https://", "").replace("http://", "").split("/")[0]
    console.print(f"\n[bold cyan]SSL Check → {host}[/bold cyan]\n")

    try:
        contexto = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=10) as sock:
            with contexto.wrap_socket(sock, server_hostname=host) as ssock:
                cert       = ssock.getpeercert()
                versao_tls = ssock.version()

        subject        = dict(x[0] for x in cert["subject"])
        issuer         = dict(x[0] for x in cert["issuer"])
        valido_ate     = datetime.strptime(cert["notAfter"],  "%b %d %H:%M:%S %Y %Z")
        valido_de      = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
        dias_restantes = (valido_ate - datetime.utcnow()).days
        san            = cert.get("subjectAltName", [])
        dominios       = ", ".join(v for t, v in san if t == "DNS")

        if dias_restantes < 0:
            status = "EXPIRADO"
        elif dias_restantes <= 30:
            status = f"EXPIRA EM {dias_restantes} DIAS"
        else:
            status = f"VÁLIDO — {dias_restantes} dias restantes"

        # exibição no terminal (igual ao que já tinha)
        console.print(f"  Status     {status}\n")
        tabela = Table(show_header=False, box=None, padding=(0, 2))
        tabela.add_column(style="dim", width=18)
        tabela.add_column(style="bold")
        tabela.add_row("Domínio",     subject.get("commonName", "N/A"))
        tabela.add_row("Emitido por", issuer.get("organizationName", "N/A"))
        tabela.add_row("Válido de",   valido_de.strftime("%d/%m/%Y"))
        tabela.add_row("Válido até",  valido_ate.strftime("%d/%m/%Y"))
        tabela.add_row("Versão TLS",  str(versao_tls))
        tabela.add_row("SANs",        dominios)
        console.print(tabela)

        return {                                     # ← devolve dicionário
            "dominio":       subject.get("commonName", "N/A"),
            "emitido_por":   issuer.get("organizationName", "N/A"),
            "valido_de":     valido_de.strftime("%d/%m/%Y"),
            "valido_ate":    valido_ate.strftime("%d/%m/%Y"),
            "dias_restantes": dias_restantes,
            "status":        status,
            "versao_tls":    str(versao_tls),
            "sans":          dominios
        }

    except ssl.CertificateError as e:
        console.print(f"[bold red]✗ Certificado inválido: {e}[/bold red]")
        return f"Certificado inválido: {e}"
    except ssl.SSLError as e:
        console.print(f"[bold red]✗ Erro SSL: {e}[/bold red]")
        return f"Erro SSL: {e}"
    except socket.timeout:
        console.print("[bold red]✗ Timeout[/bold red]")
        return "Timeout"
    except ConnectionRefusedError:
        console.print("[bold red]✗ Porta 443 fechada[/bold red]")
        return "Porta 443 fechada"
    except Exception as e:
        console.print(f"[bold red]✗ Erro inesperado: {e}[/bold red]")
        return f"Erro: {e}"