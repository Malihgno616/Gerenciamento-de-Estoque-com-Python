import sqlite3
import pandas as pd
import os

#Conecta no banco de dados
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()
#Criar tabela no banco de dados
tabela_estoque = """
CREATE TABLE IF NOT EXISTS estoque
(   
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    localizacao TEXT NOT NULL
);
"""

cursor.execute(tabela_estoque)
conn.commit()


#Classe dos Produtos que serão alterados, inseridos, adicionados ou removidos 
class GerenciamentoProduto:
    def __init__(self,id,nome,categoria,quantidade,preco,localizacao):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.preco = preco
        self.localizacao = localizacao
    
    #função para inserir um produto  no banco de dados
    def add_produto(self, produto):
        cursor.execute("""
        INSERT INTO estoque(nome, categoria, quantidade, preco, localizacao)VALUES (?, ?, ?, ?, ?);
        """, produto)
        conn.commit()

    def lista_produto(self):
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        read = "SELECT * FROM estoque"
        cursor.execute(read)
        produtos = cursor.fetchall()
        df = pd.DataFrame(produtos, columns=["id","NOME",  "CATEGORIA", "QUANTIDADE", "PREÇO", "LOCALIZAÇÃO"])
        print(df.head())
            
    # Função para atualizar um produto no banco de dados
    def atualizar_produto(self,id,preco):
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE estoque SET preco = ?WHERE id = ?", (preco, id))
        conn.commit()
        
print("GERENCIAMENTO DE ESTOQUE")

#Variáveis de inicialização para as funções das classes
id = None
nome = ""
categoria = ""
quantidade = 0
preco = 0.0
local = ""

print("""\n
    1.Inserir Produtos
    2.Lista dos Produtos
    3.Atualizar Produto
    4.Deletar Produto
    5.Relatório do Produto
    6.Sair    
    """)   

while True:
    
    opcao = int(input("Digite o número das opções acima: "))
    
    if opcao == 1:
        print("""
              Cadastre o seu produto!!! 
              Insira o id, nome, categoria, quantidade, preco e a localização!!!
        """)
        nome = str(input("Nome do produto: ")).upper()
        categoria = str(input("Categoria do produto: ")).upper()     
        quantidade = int(input("Digite a quantidade do produto: "))
        preco = float(input("Digite o preço do produto: "))
        corredor = str(input("Localização do produto, Corredor: "))
        rua = int(input("Localização do produto, Rua: "))
        local = f"Corredor: {corredor.upper()} Rua: {rua} "
        produto = GerenciamentoProduto(id,nome,categoria,quantidade,preco,local)
        produto.add_produto((nome,categoria,quantidade,preco,local))        
        
    elif opcao == 2:  
        estoque = GerenciamentoProduto(id, nome, categoria, quantidade, preco, local)
        estoque.lista_produto()
        
    elif opcao == 3:
        print("Atualizar o preço do produto")
        estoque = GerenciamentoProduto(id, nome, categoria, quantidade, preco, local)
        estoque.lista_produto()
        
        id = int(input("Digite o id do produto: "))
        preco = float(input("Digite o novo preço do produto: "))
        produto = GerenciamentoProduto(id, nome, categoria, quantidade, preco, local)
        produto.atualizar_produto(id,preco)
        
        
            
    elif opcao == 4:
        print("Escolha um produto para remover: ")
    elif opcao == 5:
        print("Relatório do produto")
    elif opcao == 6:
        print("Saindo do programa...")
        os.system('clear')
        break
    else:
        print("Opção invalida, tente novamente!")
            
