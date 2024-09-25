import uuid #para gerar IDs
import pandas as pd
import os
from db_conect import get_collection

def limpar_tela():
    # Limpa a tela de forma condicional para Windows ou sistemas Unix
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_para_visualizar():
    input("\nPressione Enter para continuar...")

livros_collection = get_collection("Livros")

def gerar_id_curto():
    return str(uuid.uuid4())[:6]  # Gerar ID curto


def add_livro():
    print("Pressione 0 em qualquer opção para cancelar a operação")
    book_id = gerar_id_curto()
    titulo = input("Insira o título do livro: ").capitalize()
    if titulo == '0':
        print("Operação cancelada.")
        return
    autor = input("Insira o nome do autor(a): ").capitalize()
    if autor == '0':
        print("Operação cancelada.")
        return
    genero = input("Insira o(s) gênero(s): ")
    if genero == '0':
        print("Operação cancelada.")
        return
    lista_generos = [gender.strip() for gender in genero.split(",")]
    ano = int(input("Insira o ano de publicação: "))
    if ano == 0:
        print("Operação cancelada.")
        return
    isbn = input("Insira o código ISBN: ")
    if isbn == '0':
        print("Operação cancelada.")
        return
    qtd = int(input("Insira a quantidade de exemplares disponíveis: "))
    if qtd == '0':
        print("Operação cancelada.")
        return

    livro = {
        '_id': book_id,
        'titulo': titulo,
        'autor': autor,
        'generos': lista_generos,
        'ano': ano,
        'ISBN': isbn,
        'qtd_disponivel': qtd
    }

    livros_collection.insert_one(livro)
    print("Livro inserido com sucesso!")


def ver_livros():
  livros = list(livros_collection.find())
  if livros:
     df = pd.DataFrame(livros)
     print("\nLivros Cadastrados\n")
     print(df[['_id', 'titulo', 'autor', 'generos', 'ano', 'ISBN', 'qtd_disponivel']].to_string(index=False))
  else:
      print("Nenhum livro encontrado.")


def atualizar_livro():
    print("Pressione 0 em qualquer opção para cancelar a operação")
    livro_id = input("Insira o ID do livro que deseja atualizar: ")
    if livro_id == '0':
        print("Operação cancelada.")
        return
    livro = livros_collection.find_one({"_id": livro_id})

    if not livro:
        print("Livro não encontrado.")
        return

    print("\nDados atuais do livro:")
    print(f"Título: {livro['titulo']}")
    print(f"Autor: {livro['autor']}")
    print(f"Gêneros: {', '.join(livro['generos'])}")
    print(f"Ano: {livro['ano']}")
    print(f"ISBN: {livro['ISBN']}")
    print(f"Quantidade disponível: {livro['qtd_disponivel']}")

    # Solicitar novas informações
    novo_titulo = input("Insira o novo título do livro (pressione Enter para manter o atual): ").capitalize()
    if novo_titulo == '0':
        print("Operação cancelada.")
        return
    novo_autor = input("Insira o novo autor(a) (pressione Enter para manter o atual): ").capitalize()
    if novo_autor == '0':
        print("Operação cancelada.")
        return
    novo_genero = input("Insira o(s) novos gênero(s) (pressione Enter para manter os atuais): ")
    if novo_genero == '0':
        print("Operação cancelada.")
        return
    novo_ano = input("Insira o novo ano de publicação (pressione Enter para manter o atual): ")
    if novo_ano == '0':
        print("Operação cancelada.")
        return
    novo_isbn = input("Insira o novo código ISBN (pressione Enter para manter o atual): ")
    if novo_isbn == '0':
        print("Operação cancelada.")
        return
    nova_qtd = input("Insira a nova quantidade de exemplares disponíveis (pressione Enter para manter a atual): ")

    # Criar um dicionário com as atualizações
    atualizacoes = {}
    if novo_titulo:
        atualizacoes['titulo'] = novo_titulo
    if novo_autor:
        atualizacoes['autor'] = novo_autor
    if novo_genero:
        atualizacoes['generos'] = [genre.strip() for genre in novo_genero.split(",")] if novo_genero else livro['generos']
    if novo_ano:
        atualizacoes['ano'] = int(novo_ano)
    if novo_isbn:
        atualizacoes['ISBN'] = novo_isbn
    if nova_qtd:
        atualizacoes['qtd_disponivel'] = int(nova_qtd)

    # Atualizar no banco de dados
    if atualizacoes:
        livros_collection.update_one({"_id": livro_id}, {"$set": atualizacoes})
        print("Livro atualizado com sucesso!")
    else:
        print("Nenhuma atualização foi realizada.")


def menu_livros():
    while True:
        print("\nLIVROS")
        print("1. Visualizar Livros\n2. Adicionar Livro\n3. Voltar\n")
        escolha = input("Escolha uma opção: ")
        limpar_tela()

        if escolha == '1':
            limpar_tela()  # Limpa a tela antes de exibir os livros
            ver_livros()
            pausar_para_visualizar()  # Dá tempo para o usuário visualizar a tabela
        elif escolha == '2':
            limpar_tela()
            add_livro()
        elif escolha == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")
            pausar_para_visualizar()