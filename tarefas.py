import sqlite3  # Importa módulo para trabalhar com SQLite

def conectar():
    # Cria conexão com banco de dados SQLite chamado 'tarefas.db'
    conn = sqlite3.connect('tarefas.db')
    return conn

def criar_tabela():
    # Cria a tabela 'tarefas' se ela ainda não existir
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID auto incrementável
        descricao TEXT NOT NULL,                -- Descrição da tarefa
        status TEXT NOT NULL,                   -- Status da tarefa (ex: pendente, concluída)
        prioridade INTEGER NOT NULL             -- Prioridade da tarefa (1 a 5)
    )
    ''')
    conn.commit()
    conn.close()

def adicionar_tarefa(descricao, status='pendente', prioridade=1):
    # Insere uma nova tarefa no banco de dados
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tarefas (descricao, status, prioridade) VALUES (?, ?, ?)
    ''', (descricao, status, prioridade))
    conn.commit()
    conn.close()

def listar_tarefas():
    # Retorna todas as tarefas ordenadas pela prioridade
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id, descricao, status, prioridade FROM tarefas ORDER BY prioridade')
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas

def atualizar_status(tarefa_id, novo_status):
    # Atualiza o status de uma tarefa pelo seu ID
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tarefas SET status = ? WHERE id = ?
    ''', (novo_status, tarefa_id))
    conn.commit()
    conn.close()

def menu():
    # Função que exibe o menu e executa as ações conforme a escolha do usuário
    criar_tabela()  # Garante que a tabela exista antes de qualquer operação

    while True:
        print("\n1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Atualizar status da tarefa")
        print("4 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            desc = input("Descrição da tarefa: ")
            pri = int(input("Prioridade (1-5): "))
            adicionar_tarefa(desc, 'pendente', pri)
            print("Tarefa adicionada com sucesso!")

        elif escolha == '2':
            tarefas = listar_tarefas()
            if tarefas:
                print("\nTarefas:")
                for t in tarefas:
                    print(f"ID: {t[0]} | Descrição: {t[1]} | Status: {t[2]} | Prioridade: {t[3]}")
            else:
                print("Nenhuma tarefa cadastrada.")

        elif escolha == '3':
            try:
                tarefa_id = int(input("ID da tarefa para atualizar o status: "))
                novo_status = input("Novo status (ex: pendente, concluída): ").strip()
                atualizar_status(tarefa_id, novo_status)
                print("Status atualizado com sucesso!")
            except ValueError:
                print("ID inválido. Tente novamente.")

        elif escolha == '4':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
