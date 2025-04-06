import json
import os
from rich.console import Console
from rich.progress import Progress

console = Console()
tarefas = []

class Tarefa:
    def __init__(self, descricao, concluida=False):
        self.descricao = descricao
        self.concluida = concluida

    def to_dict(self):
        return {"descricao": self.descricao, "concluida": self.concluida}

    @staticmethod
    def from_dict(dados):
        return Tarefa(dados["descricao"], dados["concluida"])

def listar_tarefas():
    if not tarefas:
        console.print("📭 Nenhuma tarefa cadastrada.", style="italic yellow")
        return

    console.print("\n📝 [bold underline]Lista de Tarefas:[/bold underline]")

    for i, t in enumerate(tarefas, 1):
        status = "[green]✅[/green]" if t.concluida else "[red]❌[/red]"
        console.print(f"{i}. {t.descricao} {status}")

    mostrar_progresso()

def mostrar_progresso():
    total = len(tarefas)
    concluidas = sum(1 for t in tarefas if t.concluida)

    if total == 0:
        return

    porcentagem = int((concluidas / total) * 100)

    console.print(f"\n📊 [bold]Progresso:[/bold] {concluidas}/{total} tarefas concluídas")
    with Progress(transient=True) as progress:
        barra = progress.add_task("[cyan]Progresso", total=100)
        progress.update(barra, completed=porcentagem)

ARQUIVO_TAREFAS = "tarefas.json"

def salvar_tarefas():
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tarefas], f, ensure_ascii=False, indent=2)

def carregar_tarefas():
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            tarefas.clear()
            tarefas.extend(Tarefa.from_dict(t) for t in dados)
