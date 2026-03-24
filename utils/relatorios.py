import json
import os
import sys
import subprocess
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

PASTA = Path(__file__).parent.parent / "relatorios"


def listar_arquivos():
    if not PASTA.exists():
        return []
    return sorted(PASTA.iterdir(), reverse=True)


def exibir_conteudo(arquivo: Path):
    console.print()
    console.rule(f"[bold cyan]{arquivo.name}[/bold cyan]")
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            if arquivo.suffix == ".json":
                dados = json.load(f)
                console.print_json(json.dumps(dados, ensure_ascii=False))
            else:
                console.print(f.read())
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao abrir arquivo: {e}[/bold red]")


def deletar_arquivo(arquivo: Path) -> bool:
    try:
        arquivo.unlink()
        console.print("[green]✓ Arquivo deletado.[/green]")
        return True
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao deletar: {e}[/bold red]")
        return False


def abrir_pasta():
    try:
        if sys.platform == "win32":
            os.startfile(PASTA)
        elif sys.platform == "darwin":
            subprocess.run(["open", PASTA])
        else:
            # Linux — só funciona com ambiente gráfico
            resultado = subprocess.run(
                ["xdg-open", str(PASTA)],
                capture_output=True
            )
            if resultado.returncode != 0:
                raise Exception("sem ambiente gráfico")

        console.print("[green]✓ Pasta aberta no explorador.[/green]")

    except Exception:
        # fallback — mostra o caminho pra abrir manualmente
        console.print(f"[yellow]→ Abra manualmente em: [bold]{PASTA}[/bold][/yellow]")
def exibir_menu(arquivos: list):
    texto = Text()
    for i, arquivo in enumerate(arquivos, start=1):
        cor = "cyan" if arquivo.suffix == ".json" else "green"
        texto.append(f"  {i}. ", style=f"bold {cor}")
        texto.append(f"{arquivo.name}\n")
    texto.append("\n")
    texto.append("  o. ", style="bold yellow"); texto.append("Abrir pasta no explorador\n")
    texto.append("  0. ", style="bold red");    texto.append("Voltar")

    console.print(Panel(
        texto,
        title="[bold]Relatórios[/bold]",
        subtitle=f"[dim]{len(arquivos)} arquivo(s)[/dim]",
        box=box.ROUNDED,
        border_style="cyan",
        width=70
    ))


def exibir_acoes():
    console.print()
    console.print("  [bold cyan]d.[/bold cyan] Deletar arquivo")
    console.print("  [bold cyan]o.[/bold cyan] Abrir pasta no explorador")
    console.print("  [bold cyan]Enter.[/bold cyan] Voltar à lista")


def run_relatorios():
    while True:
        console.print()
        arquivos = listar_arquivos()

        if not arquivos:
            console.print(Panel(
                "[dim]Nenhum relatório encontrado.\nGere um usando qualquer ferramenta.[/dim]",
                title="[bold]Relatórios[/bold]",
                box=box.ROUNDED,
                border_style="yellow",
                width=52
            ))
            console.input("\n[dim]Enter para voltar...[/dim]")
            break

        exibir_menu(arquivos)
        escolha = console.input("\nEscolha um arquivo (número): ").strip().lower()

        if escolha == "0":
            break

        if escolha == "o":
            abrir_pasta()
            continue

        if not escolha.isdigit() or not (1 <= int(escolha) <= len(arquivos)):
            console.print("[red]Opção inválida.[/red] Tente novamente.")
            continue

        arquivo = arquivos[int(escolha) - 1]
        exibir_conteudo(arquivo)
        exibir_acoes()

        acao = console.input("\nAção: ").strip().lower()

        if acao == "d":
            confirma = console.input(
                f"[yellow]Deletar {arquivo.name}? [s/n]: [/yellow]"
            ).strip().lower()
            if confirma == "s":
                deletar_arquivo(arquivo)

        elif acao == "o":
            abrir_pasta()