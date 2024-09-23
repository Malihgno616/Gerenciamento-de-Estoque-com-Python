import sqlite3

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
class GerenciamentoProduto():
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



print("GERENCIAMENTO DE ESTOQUE")
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
        nome = str(input("Nome do produto: ")) 
        categoria = str(input("Categoria do produto: "))     
        quantidade = int(input("Digite a quantidade do produto: "))
        preco = float(input("Digite o preço do produto: "))
        local = int(input("Localização do produto: "))
        produto = GerenciamentoProduto(id,nome,categoria,quantidade,preco,local)
        produto.add_produto((nome,categoria,quantidade,preco,local))        
        
    elif opcao == 2:
        print("Lista dos produtos")
    elif opcao == 3:
        print("Atualizar produto")    
    elif opcao == 4:
        print("Escolha um produto para remover: ")
    elif opcao == 5:
        print("Relatório do produto")
    elif opcao == 6:
        print("Saindo do programa...")
        break
    else:
        print("Opção invalida, tente novamente!")
            
