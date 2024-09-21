# No banco de dados deve incluir, nome, categoria, quantidade, preço e localização.

#Temática = Produtos Eletrônicos

#Categorias = Memória, Monitor,  Teclado, Mouse, Placa de Vídeo, Placa Mãe, Processador, Headset.
print("GERENCIAMENTO DE ESTOQUE")

import sqlite3

#Conecta no banco de dados
conn = sqlite3.connect('estoque.db')

cursor = conn.cursor()

#Criar tabela no banco de dados
tabela_estoque = """
CREATE TABLE IF NOT EXISTS estoque
(
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    localizacao TEXT NOT NULL
   
);
"""

cursor.execute(tabela_estoque)

conn.commit()

#Fecha
conn.close()

#Classe dos Produtos que serão alterados, inseridos, adicionados ou removidos 
class Produtos():
    def __init__(self,nome,categoria,quantidade,preco,localizacao):
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.preco = preco
        self.localizacao = localizacao
    
    








        