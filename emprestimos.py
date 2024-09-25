import pandas as pd
import os
from datetime import datetime, timedelta
from db_conect import get_collection
from user_management import ver_users
from book_management import ver_livros

emprestimos_collection = get_collection('emprestimos')
livros_collection = get_collection('Livros')
usuarios_collection = get_collection('Usuarios')

def limpar_tela():
    # Limpa a tela de forma condicional para Windows ou sistemas Unix
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_para_visualizar():
    input("\nPressione Enter para continuar...")


def verificar_qtd_disponivel(livro_id):
    livro = livros_collection.find_one({"_id": livro_id})
    if livro:
        print(f"Quantidade disponível: {livro['qtd_disponivel']} exemplares.")
        return livro['qtd_disponivel'] > 0
    return False


from datetime import datetime, timedelta

def registrar_emprestimo(user_id, livro_id):
    if verificar_qtd_disponivel(livro_id):
        data_emprestimo = datetime.now()
        data_devolucao = data_emprestimo + timedelta(days=14)

        emprestimo = {
            'user_id': user_id,
            'livro_id': livro_id,
            'data_emprestimo': data_emprestimo,
            'data_devolucao': None,
            'status': "Não devolvido"  # Adiciona o status aqui
        }
        
        # Debugging: Verifique se o empréstimo está sendo salvo
        print(f"Registrando empréstimo: {emprestimo}")
        emprestimos_collection.insert_one(emprestimo)
        livros_collection.update_one({"_id": livro_id}, {"$inc": {"qtd_disponivel": -1}})

        print("Empréstimo registrado com sucesso!")
    else:
        print("Não há exemplares disponíveis.")

def registrar_devolucao(user_id, livro_id):
    print(f"Buscando devolução para usuário: {user_id}, livro: {livro_id}")  # Debugging
    emprestimo = emprestimos_collection.find_one({"user_id": user_id, "livro_id": livro_id, "status": "Não devolvido"})
    
    # Debugging: Exibir todos os empréstimos para verificação
    all_emprestimos = list(emprestimos_collection.find())
    print(f"Todos os empréstimos: {all_emprestimos}")

    if emprestimo:
        print(f"Empréstimo encontrado: {emprestimo}")  # Debugging
        # Atualiza o status do empréstimo para "Devolvido"
        emprestimos_collection.update_one({"_id": emprestimo['_id']}, {"$set": {"status": "Devolvido", "data_devolucao": datetime.now()}})
        
        # Atualiza a quantidade disponível do livro
        livros_collection.update_one({"_id": livro_id}, {"$inc": {"qtd_disponivel": 1}})
        
        print("Devolução registrada com sucesso!")
    else:
        print("Empréstimo não encontrado ou já devolvido.")


def buscar_livros_por_nome(nome):
    livros = list(livros_collection.find())
    livros_filtrados = [livro for livro in livros if nome.lower() in livro['titulo'].lower()]
    
    if livros_filtrados:
        df = pd.DataFrame(livros_filtrados)
        df = df[['titulo', '_id', 'qtd_disponivel']]
        print(df)
        return df
        menu_emprestimos()
    else:
        print("Nenhum livro encontrado.")
        return None


def ver_emprestimos():
    emprestimos = list(emprestimos_collection.find())
    emprestimos_info = []

    for emprestimo in emprestimos:
        usuario = usuarios_collection.find_one({"_id": emprestimo['user_id']})
        livro = livros_collection.find_one({"_id": emprestimo['livro_id']})
        
        if usuario is None:
            print(f"Usuário com ID {emprestimo['user_id']} não encontrado.")
            continue  # Pula para o próximo empréstimo

        if livro is None:
            print(f"Livro com ID {emprestimo['livro_id']} não encontrado.")
            continue  # Pula para o próximo empréstimo

        emprestimos_info.append({
            'usuario': usuario['nome'],
            'livro': livro['titulo'],
            'data_emprestimo': emprestimo['data_emprestimo'],
            'data_devolucao': emprestimo['data_devolucao'],
            'status': 'Devolvido' if emprestimo.get('data_devolucao') else 'Não devolvido'
        })

    if emprestimos_info:
        df = pd.DataFrame(emprestimos_info)
        print(df)
        menu_emprestimos()
    else:
        print("Nenhum empréstimo encontrado.")



def menu_emprestimos():
    while True:
        print("\nEMPRÉSTIMOS")
        print("1. Buscar Livro\n2. Registrar empréstimo\n3. Registrar devolução\n4. Ver empréstimos\n5. Voltar\n")
        escolha = int(input("Escolha uma opção: "))
        limpar_tela()

        if escolha == 1:
            nome = input("Insira o nome do livro que deseja buscar: ")
            buscar_livros_por_nome(nome)
            pausar_para_visualizar()

        elif escolha == 2:
            print("Digite 0 para cancelar a operação.")
            ver_users()
            user_id = input("Insira o ID do usuário: ")
            if user_id == '0':
                print("Operação cancelada.")
                menu_emprestimos()
            ver_livros()
            livro_id = input("Insira o ID do livro: ")
            if livro_id == '0':
                print("Operação cancelada.")
                menu_emprestimos()
            registrar_emprestimo(user_id, livro_id)

        elif escolha == 3:
            print("Digite 0 para cancelar a operação.")
            ver_users()  # Para mostrar os usuários disponíveis
            user_id = input("Insira o ID do usuário: ")
            if user_id == '0':
                print("Operação cancelada.")
                continue  # Voltar ao menu sem registrar devolução
            ver_livros()  # Para mostrar os livros disponíveis
            livro_id = input("Insira o ID do livro a ser devolvido: ")
            if livro_id == '0':
                print("Operação cancelada.")
                continue  # Voltar ao menu sem registrar devolução
            registrar_devolucao(user_id, livro_id)  # Passando user_id e livro_id

        elif escolha == 4:
            ver_emprestimos()
            pausar_para_visualizar()

        elif escolha == 5:
            break
        else:
            print("Opção inválida. Tente novamente.")
