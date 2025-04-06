from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from tarefa import tarefas, Tarefa, listar_tarefas, salvar_tarefas, carregar_tarefas

# Estilo para o prompt
estilo = Style.from_dict({
    'prompt': '#00ffff bold',
    '': '#ffffff',
})

# Completer inteligente que sugere comandos ou nomes de tarefas
class ComandoCompleter(Completer):
    def get_completions(self, document, complete_event):
        texto = document.text_before_cursor.lower()
        palavras = texto.split()

        comandos = ['add', 'list', 'done', 'delete', 'save', 'exit', 'help']

        if len(palavras) <= 1:
            for cmd in comandos:
                if cmd.startswith(texto):
                    yield Completion(cmd, start_position=-len(texto))
        elif palavras[0] in ("done", "delete"):
            parte = texto[len(palavras[0]) + 1:]
            for t in tarefas:
                if t.descricao.lower().startswith(parte):
                    yield Completion(t.descricao, start_position=-len(parte))

session = PromptSession(completer=ComandoCompleter(), style=estilo)

def main():
    carregar_tarefas()
    print("✨ Gerenciador de Tarefas Interativo")
    print("Digite 'help' para ver os comandos disponíveis.")

    while True:
        try:
            entrada = session.prompt('[prompt]📌 > [/prompt]')
            partes = entrada.strip().split(" ", 1)
            comando = partes[0].lower()
            argumento = partes[1] if len(partes) > 1 else ""

            if comando == "add":
                if not argumento:
                    print("❌ Use: add <descrição>")
                    continue
                tarefas.append(Tarefa(argumento))
                print(f"✅ Tarefa adicionada: {argumento}")

            elif comando == "list":
                listar_tarefas()

            elif comando == "done":
                for t in tarefas:
                    if t.descricao == argumento:
                        t.concluida = True
                        print(f"✅ Tarefa concluída: {argumento}")
                        break
                else:
                    print("❌ Tarefa não encontrada.")

            elif comando == "delete":
                for t in tarefas:
                    if t.descricao == argumento:
                        tarefas.remove(t)
                        print(f"🗑️ Tarefa removida: {argumento}")
                        break
                else:
                    print("❌ Tarefa não encontrada.")

            elif comando == "save":
                salvar_tarefas()
                print("💾 Tarefas salvas.")

            elif comando == "help":
                print("Comandos disponíveis:")
                print("  add <descrição>    - Adiciona uma tarefa")
                print("  list               - Lista todas as tarefas")
                print("  done <descrição>   - Marca como concluída")
                print("  delete <descrição> - Remove uma tarefa")
                print("  save               - Salva as tarefas")
                print("  exit               - Sai do programa")

            elif comando == "exit":
                salvar_tarefas()
                print("👋 Saindo...")
                break

            elif comando == "":
                continue

            else:
                print("❓ Comando desconhecido. Digite 'help'.")

        except (KeyboardInterrupt, EOFError):
            print("\n👋 Encerrando.")
            break

if __name__ == '__main__':
    main()
