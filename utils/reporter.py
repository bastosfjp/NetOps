import json
from datetime import datetime
from pathlib import Path
from rich.console import Console

console = Console()

PASTA_RELATORIOS = Path(__file__).parent.parent / "relatorios"


def salvar_json(caminho: Path, ferramenta: str, alvo: str, timestamp: datetime, dados: dict):
    relatorio = {
        "ferramenta": ferramenta,
        "alvo":       alvo,
        "timestamp":  timestamp.isoformat(),
        "dados":      dados or {}
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)


def salvar_txt(caminho: Path, ferramenta: str, alvo: str, timestamp: datetime, dados: dict):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"NetOps — Relatório de {ferramenta.upper()}\n")
        f.write(f"{'=' * 40}\n")
        f.write(f"Alvo:       {alvo}\n")
        f.write(f"Timestamp:  {timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"{'=' * 40}\n\n")
        if dados:
            for chave, valor in dados.items():
                f.write(f"{chave}: {valor}\n")


def salvar_relatorio(ferramenta: str, alvo: str, formato: str, dados: dict = None):
    PASTA_RELATORIOS.mkdir(exist_ok=True)

    timestamp    = datetime.now()
    nome_arquivo = f"{ferramenta}_{alvo}_{timestamp.strftime('%Y%m%d_%H%M%S')}.{formato}"
    caminho      = PASTA_RELATORIOS / nome_arquivo

    if formato == "json":
        salvar_json(caminho, ferramenta, alvo, timestamp, dados)
    else:
        salvar_txt(caminho, ferramenta, alvo, timestamp, dados)

    console.print(f"\n[green]✓[/green] Relatório salvo em [bold]{caminho}[/bold]")


def perguntar_salvar(ferramenta: str, alvo: str, dados: dict = None):
    resposta = console.input("\nSalvar resultado? ([bold green]s[/bold green]/[bold red]n[/bold red]): ").strip().lower()

    if resposta != "s":
        return

    formato = console.input("Formato — [bold]json[/bold] ou [bold]txt[/bold]: ").strip().lower()

    if formato not in ["json", "txt"]:
        console.print("[red]✗ Formato inválido. Digite 'json' ou 'txt'.[/red]")
        return

    salvar_relatorio(ferramenta, alvo, formato, dados)