import json
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

ARQUIVO_HISTORICO = Path(__file__).parent.parent / "historico.json"
MAX_ENTRADAS = 50


# ─── leitura e escrita ───────────────────────────────────────────────────────

def carregar_historico() -> list:
    try:
        if ARQUIVO_HISTORICO.exists():
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def salvar_historico(historico: list):
    try:
        with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
            json.dump(historico, f, indent=2, ensure_ascii=False)
    except Exception as e:
        console.print(f"[yellow]⚠ Não foi possível salvar histórico: {e}[/yellow]")


# ─── registro de execução ────────────────────────────────────────────────────

def registrar(ferramenta: str, alvo: str, status: str):
    historico = carregar_historico()

    entrada = {
        "ferramenta": ferramenta,
        "alvo":       alvo,
        "timestamp":  datetime.now().isoformat(),
        "status":     status
    }

    historico.insert(0, entrada)          # mais recente no topo
    historico = historico[:MAX_ENTRADAS]  # mantém só as últimas 50
    salvar_historico(historico)


# ─── exibição ────────────────────────────────────────────────────────────────

def formatar_status(status: str) -> Text:
    texto = Text()
    if status == "sucesso":
        texto.append("sucesso", style="bold green")
    elif status == "timeout":
        texto.append("timeout", style="bold yellow")
    else:
        texto.append("erro",    style="bold red")
    return texto


def exibir_detalhe(entrada: dict):
    console.print()
    console.rule("[bold cyan]Detalhe[/bold cyan]")

    tabela = Table(show_header=False, box=None, padding=(0, 2))
    tabela.add_column(style="dim",  width=14)
    tabela.add_column(style="bold")

    dt = datetime.fromisoformat(entrada["timestamp"])

    tabela.add_row("Ferramenta", entrada["ferramenta"].upper())
    tabela.add_row("Alvo",       entrada["alvo"])
    tabela.add_row("Data",       dt.strftime("%d/%m/%Y"))
    tabela.add_row("Hora",       dt.strftime("%H:%M:%S"))
    tabela.add_row("Status",     formatar_status(entrada["status"]))

    console.print(tabela)


def run_historico():
    while True:
        console.print()
        historico = carregar_historico()

        if not historico:
            console.print(Panel(
                "[dim]Nenhuma execução registrada ainda.\nUse qualquer ferramenta para começar.[/dim]",
                title="[bold]Histórico[/bold]",
                box=box.ROUNDED,
                border_style="yellow",
                width=52
            ))
            console.input("\n[dim]Enter para voltar...[/dim]")
            break

        # ─── monta a tabela de listagem ──────────────────────────────────
        tabela = Table(
            "#", "Data", "Hora", "Ferramenta", "Alvo", "Status",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE,
            padding=(0, 1)
        )

        for i, entrada in enumerate(historico, start=1):
            dt     = datetime.fromisoformat(entrada["timestamp"])
            data   = dt.strftime("%d/%m")
            hora   = dt.strftime("%H:%M")
            status = formatar_status(entrada["status"])

            tabela.add_row(
                str(i),
                data,
                hora,
                entrada["ferramenta"].upper(),
                entrada["alvo"],
                status
            )

        console.print(Panel(
            tabela,
            title="[bold]Histórico de execuções[/bold]",
            subtitle=f"[dim]{len(historico)} registro(s) — máx. {MAX_ENTRADAS}[/dim]",
            box=box.ROUNDED,
            border_style="cyan"
        ))

        console.print("\n  [bold cyan]número[/bold cyan] Ver detalhe   [bold red]0[/bold red] Voltar")
        escolha = console.input("\nEscolha: ").strip()

        if escolha == "0":
            break

        if not escolha.isdigit() or not (1 <= int(escolha) <= len(historico)):
            console.print("[red]Opção inválida.[/red] Tente novamente.")
            continue

        exibir_detalhe(historico[int(escolha) - 1])
        console.input("\n[dim]Enter para voltar...[/dim]")