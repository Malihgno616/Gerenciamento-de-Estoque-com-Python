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
    marca TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    localizacao TEXT NOT NULL,
    data_cadastro DATE NOT NULL DEFAULT (date('now'))
);
"""

cursor.execute(tabela_estoque)
conn.commit()

#Classe dos Produtos que serão alterados, inseridos, adicionados ou removidos 
class GerenciamentoProduto:
    def __init__(self,id,nome,categoria,marca,quantidade,preco,localizacao,data=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.marca = marca
        self.quantidade = quantidade
        self.preco = preco
        self.localizacao = localizacao
        self.data = data
    
    #função para inserir um produto  no banco de dados
    def add_produto(self, produto):
        cursor.execute("""
        INSERT INTO estoque(nome, categoria, marca, quantidade, preco, localizacao, data_cadastro)VALUES (?, ?, ?, ?, ?, ?, date('now'));
        """, produto)
        conn.commit()

    def lista_produto(self):
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        read = "SELECT * FROM estoque"
        cursor.execute(read)
        produtos = cursor.fetchall()
        df = pd.DataFrame(produtos, columns=["id","NOME","CATEGORIA","MARCA","QUANTIDADE","PREÇO", "LOCALIZAÇÃO", "DATA DE CADASTRO"])
        print(df.head())
            
    # Função para atualizar um produto no banco de dados
    def atualizar_produto(self,id,preco):
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE estoque SET preco = ?WHERE id = ?", (preco, id))
        conn.commit()
    
    def deletar_produto(self, id):
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estoque WHERE id = ?", (id,))
        conn.commit()       
       
print("GERENCIAMENTO DE ESTOQUE")

#Variáveis de inicialização para as funções das classes
id = None
nome = ""
marca = ""
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
    
    # Cadastrar o produto para adicionar para o banco de dados
    if opcao == 1:
        print("""
              Cadastre o seu produto!!! 
              Insira o id, nome, categoria, quantidade, preco e a localização!!!
        """)
        nome = str(input("Nome do produto: ")).upper()
        categoria = str(input("""
        Escolha uma das opções de categoria do produto;\n
        Televisão, Console de Jogos, Leitores de Mídia, Tablet, Smartphone, Sistemas de Áudio, Pen Drives e Cartões de Memória\nEscolha: """)).upper()        
        marca = str(input("Digite a marca do produto: ")).upper()     
        quantidade = int(input("Digite a quantidade do produto: "))
        preco = float(input("Digite o preço do produto: "))
        corredor = str(input("Localização do produto, Corredor: "))
        rua = int(input("Localização do produto, Rua: "))
        local = f"Corredor: {corredor.upper()} Rua: {rua} "
        produto = GerenciamentoProduto(id,nome,categoria,marca,quantidade,preco,local)
        produto.add_produto((nome,categoria,marca,quantidade,preco,local))        
    
    #Opção para exibir a lista do banco de dados por pandas    
    elif opcao == 2:  
        estoque = GerenciamentoProduto(id, nome, categoria,marca,quantidade, preco, local)
        estoque.lista_produto()
        
    #Opção para atualizar o preço do produto pelo id    
    elif opcao == 3:
        print("Atualizar o preço do produto")
        estoque = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local)
        estoque.lista_produto()
        id = int(input("Digite o id do produto: "))
        preco = float(input("Digite o novo preço do produto: "))
        produto = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local).date.today()
        produto.atualizar_produto(id,preco)
        print("Preço atualizado com sucesso!!!")
              
    #Opção para remover um produto do banco de dados        
    elif opcao == 4:
        print("Escolha um produto para remover: ")
        estoque = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local)
        estoque.lista_produto()
        id = int(input("Escolha um produto pelo id para remover do banco de dados: "))
        estoque.deletar_produto(id)
        
    elif opcao == 5:
        print("Relatório do produto")
    elif opcao == 6:
        print("Saindo do programa...")
        os.system('clear') or None
        break
        
    else:
        print("Opção invalida, tente novamente!")
            
