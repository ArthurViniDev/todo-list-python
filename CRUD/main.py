from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from tarefa import tarefas, Tarefa, listar_tarefas, salvar_tarefas, carregar_tarefas

# Estilo para o prompt
estilo = Style.from_dict({
    'prompt': '#00ffff bold',
    '': '#ffffff',
})

# Comandos disponíveis
comandos = ['add', 'list', 'done', 'save', 'exit', 'help']
completer = WordCompleter(comandos, ignore_case=True)

# Sessão do prompt
session = PromptSession(completer=completer, style=estilo)

def main():
    carregar_tarefas()
    print("✨ Gerenciador de Tarefas Interativo com prompt_toolkit")
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

            elif comando == "save":
                salvar_tarefas()
                print("💾 Tarefas salvas.")

            elif comando == "help":
                print("Comandos disponíveis:")
                print("  add <descrição> - Adiciona uma tarefa")
                print("  list            - Lista todas as tarefas")
                print("  done <descrição>- Marca como concluída")
                print("  save            - Salva as tarefas")
                print("  exit            - Sai do programa")

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
