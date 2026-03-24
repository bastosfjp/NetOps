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

def run_dns(host: str):
    console.print(f"\n[bold cyan]DNS Lookup → {host}[/bold cyan]\n")

    tipos  = ["A", "AAAA", "MX", "NS", "TXT"]
    tabela = Table("Tipo", "Valor", "TTL")
    registros = []                                  # ← guarda os registros

    for tipo in tipos:
        try:
            respostas = dns.resolver.resolve(host, tipo)
            for r in respostas:
                tabela.add_row(tipo, str(r), str(respostas.ttl))
                registros.append(f"{tipo}: {str(r)}")   # ← guarda cada um
        except Exception:
            pass

    console.print(tabela)

    if not registros:
        return f"Nenhum registro encontrado para {host}"

    return "\n".join(registros)                     # ← devolve tudo