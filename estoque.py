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

    #Exibe a tabela do produto do banco de dados
    def lista_produto(self):
        cursor.execute("SELECT * FROM estoque")
        produtos = cursor.fetchall()
        df = pd.DataFrame(produtos, columns=["id","NOME","CATEGORIA","MARCA","QUANTIDADE","PREÇO", "LOCALIZAÇÃO", "DATA DE CADASTRO"])
        print(df)
            
    # Função para atualizar um produto no banco de dados
    def atualizar_produto(self,id,quantidade):
        cursor.execute("UPDATE estoque SET quantidade = quantidade + ? WHERE id = ?", (quantidade, id))
        conn.commit()
    
    # Função para vender uma quantia específica de produtos baseados no id e quantidade
    def vender_produto(self, id, quantidade):
        cursor.execute("UPDATE estoque SET quantidade = quantidade - ? WHERE Id = ?", (quantidade, id)) 
        conn.commit()
        
    # Função da classe que deleta um produto do banco de dados
    def deletar_produto(self, id):
        cursor.execute("DELETE FROM estoque WHERE id = ?", (id,))
        conn.commit()       
    
    def relatorio_produto(self):
        estoque_baixo = 5
        estoque_excesso = 50
        
        cursor.execute("SELECT * FROM estoque WHERE quantidade < ?",(estoque_baixo,))
        baixo = cursor.fetchall()
        
        cursor.execute("SELECT * FROM estoque WHERE quantidade > ?",(estoque_excesso,))
        excesso = cursor.fetchall()

        print("=== Relatório de Estoque ===")
        print("\nEstoque Baixo:")
        if baixo:
            for produto in baixo:
                print(f"""ID:{produto[0]} Nome:{produto[1]}, Quantidade:{produto[4]} Localização:{produto[6]} """)
        else:
            print("Nenhum produto com estoque baixo encontrado.")      
        
        print("\nExcesso de Estoque:")                
        if excesso:
            for produto in excesso:
                print(f"""ID:{produto[0]} Nome:{produto[1]} Quantidade: {produto[4]} Localização:{produto[6]} """)
        else:
            print("Nenhum produto com excesso de estoque encontrado.")
    
    def local_produto(self, id):
        cursor.execute("SELECT localizacao FROM estoque WHERE id = ?", (id,))
        local = cursor.fetchone()  # Use fetchone para obter um único resultado
        if local:
            print(f"""
                  Localização do produto ID: {id}: {local[0]}
                  """)
        else:
            print("Produto não encontrado.")

        
        
    
print("GERENCIAMENTO DE ESTOQUE")

#Variáveis de inicialização para as funções das classes
id = None
nome = ""
marca = ""
categoria = ""
quantidade = 0
preco = 0.0
local = ""

while True:
    
    opcao = int(input("""
            1.Inserir Produtos
            2.Lista dos Produtos
            3.Atualizar Produto
            4.Deletar Produto
            5.Relatório do Produto
            6.Localização
            7.Vender
            8.Sair
               
            Digite o número das opções acima: """))
    
    # Cadastrar o produto para adicionar para o banco de dados
    if opcao == 1:
        print("""
              Cadastre o seu produto!!! 
              Insira o nome
              categoria
              quantidade
              preco 
              e a localização!!!
        """)
        nome = str(input("Nome do produto: ")).upper()
        categoria = str(input("""
        Escolha uma das opções de categoria do produto:
        Televisão
        Console de Jogos 
        Leitores de Mídia
        Tablet, Smartphone
        Sistemas de Áudio 
        Pen Drives
        Cartões de Memória
        Monitor 
        Teclado
        Mouse
        Placa de Vídeo 
        Placa Mãe
        Processador 
        Headset
        Escolha: """)).upper()
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
        voltar = input("\nDeseja voltar para o menu principal?: (sim/não) ")
        if voltar == "sim":
            continue
        else:
            os.system('clear') or None
            break       
        
    #Opção para atualizar o preço do produto pelo id    
    elif opcao == 3:
        print("Atualizar o preço do produto")
        estoque = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local)
        estoque.lista_produto()
        id = int(input("Digite o id do produto: "))
        quantidade = float(input("Quantidade novo do produto: "))
        produto = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local)
        produto.atualizar_produto(id,quantidade)
                      
    #Opção para remover um produto do banco de dados        
    elif opcao == 4:
        print("Escolha um produto para remover: ")
        estoque = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local)
        estoque.lista_produto()
        id = int(input("Escolha um produto pelo id para remover do banco de dados: "))
        estoque.deletar_produto(id)
        
    elif opcao == 5:
        print("Relatório do produto")
        estoque = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local)
        estoque.relatorio_produto()
        voltar = input("\nDeseja voltar para o menu principal?: (sim/não) ")
        if voltar == "sim":
            continue
        else:
            break
        
    elif opcao == 6:
        print("Localização do produto")
        estoque = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local)
        estoque.lista_produto()
        id = int(input("Digite o id do produto que deseja saber a localização: "))
        estoque.local_produto(id)
        voltar = input("\nDeseja voltar para o menu principal?: (sim/não) ")
        if voltar == "sim":
            continue
        else:
            os.system('clear') or None
            break
        
    elif opcao == 7:
        print("Vender um produto")
        estoque = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local)
        estoque.lista_produto()
        id = int(input("Digite o id do produto: "))
        quantidade = float(input("Quanto irá ser vendido: "))
        produto = GerenciamentoProduto(id, nome, categoria,marca, quantidade, preco, local)
        produto.vender_produto(id,quantidade)
                
    elif opcao == 8:
        print("Saindo do programa...")
        os.system('clear') or None
        break
        
    else:
        print("Opção invalida, tente novamente!")
            
