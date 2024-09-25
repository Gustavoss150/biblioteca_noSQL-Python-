import uuid #para gerar IDs
import re
import pandas as pd
import os
from datetime import datetime, timedelta

from db_conect import get_collection
usuarios_collection = get_collection('Usuarios')

def limpar_tela():
    # Limpa a tela de forma condicional para Windows ou sistemas Unix
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_para_visualizar():
    input("\nPressione Enter para continuar...")

def gerar_id_curto():
    return str(uuid.uuid4())[:6]  # Gerar ID curto


def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf) # remover pontos e traços
    if len(cpf) == 11:
        return True
    else:
        return False
    
    
def validar_email(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' # define possibilidades de caracteres
    return re.match(padrao, email) is not None


def validar_dataNasc(data_nascimento):
    try:
        datetime.strptime(data_nascimento, "%d/%m/%Y")
        return True
    except ValueError:
        return False
    
    
def cadastrar_user():
    print ("Pressione 0 em qualquer opção para cancelar operação.")
    user_id = gerar_id_curto()
    nome = input("Insira o nome completo: ").capitalize()
    if nome == '0':
        print("Operação cancelada.")
        return
    
    email = input("Insira o E-mail: ")
    if email == '0':
        print("Operação cancelada.")
        return
    while not validar_email(email):
        print("E-mail inválido. Tente novamente.")
        email = input("Insira o E-mail: ")
        if email == '0':
            print("Operação cancelada.")
            return

    data_nascimento = input("Insira a data de nascimneto (dd/mm/aaaa): ")
    if data_nascimento == '0':
        print("Operação cancelada.")
        return
    while not validar_dataNasc(data_nascimento):
        print("Data de nascimento inválida. Tente novamente.")
        data_nascimento = input("Insira a data de nascimento (dd/mm/aaaa): ")
        if data_nascimento == '0':
            print("Operação cancelada.")
            return

    documento = input("Insira o CPF (somente números): ")
    if documento == '0':
        print("Operação cancelada.")
        return
    while not validar_cpf(documento):
        print("Documento inválido. Tente novamente.")
        documento = input("Insira o CPF (somente números): ")
        if documento == '0':
            print("Operação cancelada.")
            return

    # Salvando dados do usuário
    usuario = {
        '_id': user_id,
        'nome': nome,
        'e-mail': email,
        'data_de_nascimento': data_nascimento,
        'documento': documento
    }

    # Inserir no banco de dados (coleção Usuarios)
    usuarios_collection.insert_one(usuario)
    print("Usuário cadastrado com sucesso!")
    print(usuario)

def ver_users():
    usuarios = list(usuarios_collection.find())
    if usuarios:
        df = pd.DataFrame(usuarios)
        print("\nUsuários Cadastrados\n")
        print(df[['_id', 'nome', 'e-mail', 'data_de_nascimento', 'documento']].to_string(index=False))  # Exibir apenas as colunas desejadas
    else:
        print("Nenhum usuário encontrado.")

def remove_user():
    ver_users()
    print ("Pressione 0 em qualquer opção para cancelar operação.")
    documento = input("Informe o CPF do usuário a ser removido (apenas números): ")
    # Remove qualquer ponto ou traço do CPF inserido
    documento = re.sub(r'\D', '', documento)  # Remove todos os caracteres que não são números
    if documento == '0':
        print("Operação cancelada.")
        return

    result = usuarios_collection.delete_one({"documento": documento})
    if result.deleted_count > 0:
        print("Usuário removido com sucesso.")
    else:
        print("Usuário não encontrado.")

def atualizar_cadastro():
    ver_users()
    print("Pressione 0 para cancelar operação.")
    user_id = input("Insira o ID do usuário que deseja atualizar: ")
    
    if user_id == '0':
        print("Operação cancelada.")
        return

    user = usuarios_collection.find_one({"_id": user_id})
    if not user:
        print("Usuário não encontrado.")
        return
    
    print("Dados atuais do usuário:")
    print(f"Nome: {user['nome']}")
    print(f"E-mail: {user['e-mail']}")
    print(f"Data de Nascimento: {user['data_de_nascimento']}")
    print(f"Documento: {user['documento']}\n")

    novo_nome = input("Insira o nome do usuário (pressione Enter para manter o atual): ").capitalize() or user['nome']
    novo_email = input("Insira o novo e-mail (pressione Enter para manter o atual): ") or user['e-mail']
    
    if novo_email and not validar_email(novo_email):
        print("E-mail inválido. Tente novamente.")
        return  # Encerra a função se o e-mail for inválido

    nova_data_nasc = input("Insira a data de nascimento (dd/mm/aaaa) (pressione Enter para manter o atual): ") or user['data_de_nascimento']
    
    if nova_data_nasc and not validar_dataNasc(nova_data_nasc):
        print("Data de nascimento inválida. Tente novamente.")
        return  # Encerra a função se a data for inválida

    novo_documento = input("Insira o documento (pressione Enter para manter o atual): ") or user['documento']
    
    if novo_documento and not validar_cpf(novo_documento):
        print("Documento inválido. Tente novamente.")
        return  # Encerra a função se o CPF for inválido

    # Criar um dicionário com as atualizações
    atualizacoes = {
        'nome': novo_nome,
        'e-mail': novo_email,
        'data_de_nascimento': nova_data_nasc,
        'documento': novo_documento
    }

    # Atualiza no banco de dados
    usuarios_collection.update_one({"_id": user_id}, {"$set": atualizacoes})
    print("Cadastro atualizado com sucesso!")


def menu_usuarios():
    while True:
        print("\nUSUÁRIOS\n1. Visualizar Cadastros\n2. Novo Cadastro\n3. Atualizar Cadastro\n4. Remover Cadastro\n5. Voltar")
        escolha = int(input("Escolha uma opção: "))
        limpar_tela()

        if escolha == 1:
            ver_users()
            pausar_para_visualizar()
            break
        elif escolha == 2:
            cadastrar_user()
        elif escolha == 3:
            atualizar_cadastro()
        elif escolha == 4:
            remove_user()
        elif escolha == 5:
            break
        else:
            print("Opção inválida. Tente novamente")
    