import json
import os

ARQUIVO = "tarefas.json"
tarefas = []

class Tarefa:
    def __init__(self, descricao, concluida=False):
        self.descricao = descricao
        self.concluida = concluida

    def to_dict(self):
        return {"descricao": self.descricao, "concluida": self.concluida}

def listar_tarefas():
    if not tarefas:
        print("⚠️ Nenhuma tarefa encontrada.")
        return
    for i, t in enumerate(tarefas, 1):
        status = "✅" if t.concluida else "❌"
        print(f"{i}. {t.descricao} [{status}]")

def salvar_tarefas():
    with open(ARQUIVO, "w") as f:
        json.dump([t.to_dict() for t in tarefas], f)

def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            dados = json.load(f)
            tarefas.clear()
            for item in dados:
                tarefas.append(Tarefa(item["descricao"], item["concluida"]))
