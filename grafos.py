# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 23:16:47 2020

@author: Ada Silva
"""

import sys
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Removendo a impressão dos warnings
import warnings
warnings.filterwarnings("ignore")
    
# Classe Grafo
# - direcionado: identifica se o grafo é direcionado ou não {True, False} 
# - matriz_adjacente: pandas.dataframe estrutura de dados criada para armazenar a matriz de adjacência 
# - dicionario_vertices: dicionário para armazenar todos os nomes dos vértices do grafo

class Grafo:
    
    direcionado = False
    matriz_adjacente = False
    dicionario_vertices = {} 
    visitado = False
    g = nx.DiGraph()    
    
    def __init__(self, lista_linhas):
        
        if len(lista_linhas) > 0:
        # Primeira linha é para identificar se o grafo é direcionado ou não
            if lista_linhas[0] == "D":
                self.direcionado = True
            
            index = 0
        
            # Todas as outras linhas do arquivo são para inserir vértices     
            
            for line in lista_linhas[1:]:
                linha_limpa = line.replace(" ", "") # Limpa a linha 
                vertices = linha_limpa.split(",")   # Cria array de vértices
                
                # Percorre todos os vertices para inserir em um dicionário de vértices
                for vertice in vertices:
                    if vertice:
                        if vertice not in self.dicionario_vertices.values(): # Adiciona um vertice se ainda não foi adicionado
                            self.dicionario_vertices[index] = vertice
                            # insere novo index
                            index+=1
            
            # Constroi a matriz com 0                 
            self.construir_matriz()
            
            # Percorre com for para inserir os vértices 
            for linha in lista_linhas[1:]:
                linha_limpa = linha.replace(" ", "")
                vertices = linha_limpa.split(",")

                if len(vertices) == 2:
                    self.matriz_adjacente[vertices[0]][vertices[1]] = 1
                    
                    if not self.direcionado: # Se não for direcionado, a matriz é preenchida tanto no grau de saída, como no de entrada
                        self.matriz_adjacente[vertices[1]][vertices[0]] = 1
                    
                    self.g.add_edge(vertices[0], vertices[1])
        
                    
    # verifica_adjacencia
    # - Recebe v1, v2 como o vértice 1 e o vértice 2
    # - Descobre se dois vértices são adjacentes    
    # - Não retorna nada        
    def verifica_adjacencia(self, v1, v2):
        
        if (v1 in self.dicionario_vertices.values()) and (v2 in self.dicionario_vertices.values()):
            if (self.matriz_adjacente[v1][v2] == 1) or (self.matriz_adjacente[v2][v1] == 1):
                print(str(v1) + " e " + str(v2) + " são adjacentes")
            else:
                print(str(v1) + " e " + str(v2) + " não são adjacentes")
        else:
            print("Vértice não encontrado")
    
    
    # grau_vertice
    # - Recebe vertice
    # - Descobre o grau do vertice escolhido 
    # - Não retorna nada
    def grau_vertice(self, vertice):
        print("")
        print("GRAU DO VÉRTICE "  + vertice)
        if vertice in self.dicionario_vertices.values():
            if not self.direcionado:
                grau = np.sum(self.matriz_adjacente[vertice])  
                print(self.matriz_adjacente[:][vertice])
                print('Grau:' + str(grau))    
            else:
                
                print("Grau de entrada: " + str(np.sum(self.matriz_adjacente.loc[vertice, :])))
                print("Grau de saída: " + str(np.sum(self.matriz_adjacente.loc[:, vertice])))
                
        else:
            print("Vértice não encontrado.")
    



    def imprime_todos_nos(self):
        
        if len(self.dicionario_vertices) > 0:    
            colunas = [False] * len(self.dicionario_vertices)
            linhas = [colunas] * len(self.dicionario_vertices)
            self.visitado =  pd.DataFrame(np.array(linhas), columns=self.dicionario_vertices.values(), index=self.dicionario_vertices.values())
            self.visita_todas_arestas(self.dicionario_vertices[0])   
            
            
    # visita_todas_arestas
    # - Recebe origem de busca
    # - Função recursiva para percorrer todos os nós 
    # - Não retorna nada
    def visita_todas_arestas(self, origem):
        
        
        for adj in self.matriz_adjacente[origem].index:
            if self.matriz_adjacente[origem][adj] == 1:
                if self.visitado[origem][adj] == False:             
                    self.visitado[origem][adj] = True
                    print("{" + origem + ", " + adj + "}")
                    self.visita_todas_arestas(adj)
         
        
    
    # grau_vertice
    # - Recebe vertice
    # - Encontra vizinhos desse vertice
    # - Não retorna nada
    def encontra_vizinhos(self, vertice):
        print("")
        print("VIZINHO DO VÉRTICE "  + vertice)
        if vertice in self.dicionario_vertices.values():
            print("-------------------------------------------------------------------------")
            
            if self.direcionado == False:
                for candidato_vizinho in self.matriz_adjacente[vertice].index:
                    if self.matriz_adjacente[vertice][candidato_vizinho] == 1:
                        print(candidato_vizinho)
            else:
                print("Vizinho Sucessor")
                for candidato_vizinho in self.matriz_adjacente[vertice].index:
                    if self.matriz_adjacente[vertice][candidato_vizinho] == 1:
                        print(candidato_vizinho)
                        
                print("Vizinho Antecessor")
                for candidato_vizinho in self.matriz_adjacente[vertice].index:
                    if self.matriz_adjacente[candidato_vizinho][vertice] == 1:
                        print(candidato_vizinho)        
            print("-------------------------------------------------------------------------")        
        else:
            print("Vértice não encontrado.")      
       
     
        
    # construir_matriz
    # - Constroi matriz n x m com zeros 
    # - Não retorna nada    
    def construir_matriz(self):
       
        colunas = [0] * len(self.dicionario_vertices)
        linhas = [colunas] * len(self.dicionario_vertices)
        self.matriz_adjacente = pd.DataFrame(np.array(linhas), columns=self.dicionario_vertices.values(), index=self.dicionario_vertices.values())
        
        
        
    # desenhar grafo
    # - desenha um grafo com a lib networkx
    # - Não retorna nada    
    def desenhar_grafo(self):
        
        
        
        if not self.direcionado:
            self.g = self.g.to_undirected()
            
        nx.draw(self.g,with_labels=True)
        plt.draw()
        plt.show()
        
    
    # print_matriz
    # - Imprime a matriz de adjacência preenchida 
    # - Não retorna nada     
    def print_matriz(self):
        
        print("")
        print("MATRIZ DE ADJACÊNCIA")
        print("-------------------------------------------------------------------------")      
        print(self.matriz_adjacente)
        print("-------------------------------------------------------------------------")  
        if self.direcionado:
            print("Grafo Dirigido")
        else:
            print("Grafo Não Dirigido")
            
def leitura_arquivos_para_grafos(lista_linhas):
       g1 = nx.DiGraph()  
       
       if len(lista_linhas) > 0:
        # Primeira linha é para identificar se o grafo é direcionado ou não
            if lista_linhas[0] == "ND":
                g1 = g1.to_undirected() 
            
        
            # Todas as outras linhas do arquivo são para inserir vértices     
            
            for line in lista_linhas[1:]:
                linha_limpa = line.replace(" ", "") # Limpa a linha 
                vertices = linha_limpa.split(",")   # Cria array de vértices
                g1.add_edge(vertices[0], vertices[1])
               
            nx.draw(g1,with_labels=True)
            plt.draw()
            plt.show()    
                
                
                       


def main():
    
    
    print("Qual o nome do arquivo? Ex: teste.txt")
    input_file = input()    
                
    lista_linhas = leitura_arquivo(input_file)
                
    g = Grafo(lista_linhas)
                
    while(True):
        print("")
        print("")
        print("Menu")
        print("[1] Imprimir matriz de grafos")
        print("[2] Calcular o grau de um vértice")
        print("[3] Buscar todos os vizinhos de um vértice")
        print("[4] Visitar todas as arestas do grafo")
        print("[5] Verificar se dois vértices são adjacentes")
        print("[6] Desenhar Grafo")
        print("[7] Sair")
        opcao = input()
        
        if opcao == '1':
            print("")
            g.print_matriz()
        
        if opcao == '2':
            print("")
            print("Insira um vértice:")
            vertice = input()
            g.grau_vertice(vertice)
        
        if opcao == '3':
            print("Insira um vértice:")
            vertice = input()
            g.encontra_vizinhos(vertice)
        
        if opcao == '4':
            print("")
            g.imprime_todos_nos()
            
        
        if opcao == '5':
            print("")
            print("Digite o primeiro vértice")
            v1 = input()
            print("Digite o segundo vértice")
            v2 = input()
            g.verifica_adjacencia(v1, v2)
            
        if opcao == '6':
            print("")
            print("Desenhar o gráfico do arquivo já inserido(s/n)?")
            opc = input()
            if opc == 'n':
                print("Insira o caminho do arquivo. Ex: C:/user/Desktop/grafo.txt")
                arquivo = input()
                lista_files = leitura_arquivo(arquivo)
                if len(lista_files) > 0:
                    leitura_arquivos_para_grafos(lista_files)
            if opc == 's':
                g.desenhar_grafo()
                
        if opcao == '7':
            print("Bye.")
            sys.exit(2)
         
        print("Voltar para menu inicial[s/n]")
        opc = input()    
        while opc != 's':
            opc = input()
        
    
        
        
# Função leitura_arquivo 
# Parâmetro: url - caminho do arquivo        
# Returns: linha_linhas - lista de todas as linhas do arquivo           
def leitura_arquivo(url):
    
   lista_linhas = []
   try:
       arquivo = open(url, "r")
       print("Arquivo carregado.")
       for linha in arquivo:
           linha = linha.replace('\n', '')
           lista_linhas.append(linha)  
   except:
        print('Problema na leitura do arquivo.')
         
   return lista_linhas           



if __name__ == "__main__":
   main()    
     