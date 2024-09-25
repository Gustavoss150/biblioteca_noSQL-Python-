import os
from user_management import menu_usuarios
from book_management import menu_livros
from emprestimos import menu_emprestimos

def limpar_tela():
    # Limpa a tela de forma condicional para Windows ou sistemas Unix
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_para_visualizar():
    input("\nPressione Enter para continuar...")


def menu():
    while True:
        print("\nMENU\n1. Usuários\n2. Livros\n3. Empréstimos\n4. Sair")
        escolha = int(input("Escolha uma opção: "))
        limpar_tela()

        if escolha == 1:
            menu_usuarios()
        elif escolha == 2:
            menu_livros()
        elif escolha == 3:
            menu_emprestimos()
        elif escolha == 4:
            break

if __name__ == "__main__":
    menu()

    import requests

