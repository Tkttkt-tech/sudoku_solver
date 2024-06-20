import pandas as pd
import numpy as np
import datetime
from copy import deepcopy

def solver(new_sudoku,log=False):
  inicio = datetime.datetime.now()
  sudoku,pilha, guess_sudoku, pilha_guess,flag = inicia_sudoku(new_sudoku)
  stop_counter = 1
  max_pilha = 0
  display('Sudoku Inicial: ', sudoku)
  while flag == 1 and stop_counter <= 200:
    sudoku = deepcopy(pilha[-1]) #Sudoku mais atual
    guess_sudoku = deepcopy(pilha_guess[-1]) #Guess mais atual
    if log:
      print('Iteracao', stop_counter)
      display('Sudoku Inicio Iteracao:',sudoku)
    sudoku = add_obvios(sudoku) #Adiciona obvios
    if sudoku != pilha[-1]:
      if log:
        print('Obvios Adicionados.')
    if check(sudoku): #Fecha se Sudoku estiver terminado depois do obvio
      flag = 0
      display(sudoku)
      pilha = empilha(pilha,sudoku)
      break

    i,j,sudoku,guess_sudoku = insert_guess(sudoku,guess_sudoku) #Insere um guess

    pilha = empilha(pilha,sudoku) #Empilha Sudoku e Guess
    pilha_guess = empilha(pilha_guess,guess_sudoku)

    #Erro tipo 1 (Trocar de chute)
    if small_pencil_size(pilha[-1]):
      if log:
        print('Impossivel de continuar. Voltando 1 Sudoku.')
      pilha = desempilha(pilha)

    futuro_estimado = deepcopy(pilha[-1])
    futuro_estimado = add_obvios(futuro_estimado)
    if check(futuro_estimado): #Fecha se Sudoku estiver terminado depois do obvio
      flag = 0
      display(futuro_estimado)
      pilha = empilha(pilha,futuro_estimado)
      
      break

    #Se removermos 1 guess, precisamos remover todos os guess que ja estavam em seu limite
    while small_pencil_size(futuro_estimado) == True and ~check(sudoku): #Se for verificado que ainda nao terminou E com o proximo obvio vai dar pau 
      if log:
        print('Impossivel de continuar. Voltando 1 Sudoku.')
      pilha = desempilha(pilha) #Desempilhar
      futuro_estimado = deepcopy(pilha[-1])
      futuro_estimado = add_obvios(futuro_estimado) #E verificar como o procimo proximo obvio vai ficar.
      while check_backtrack(futuro_estimado, pilha_guess[-1]): #Se não tiver mais valores possiveis no proximo local com o guess atual. trocar esse with por um while! 
        pilha = desempilha(pilha)
        vazios_inicial = count_guess_vazios(pilha_guess[-1])
        pilha_guess = desempilha(pilha_guess)
        while(vazios_inicial == count_guess_vazios(pilha_guess[-1])):
          pilha_guess = desempilha(pilha_guess)
        futuro_estimado = deepcopy(pilha[-1])
        futuro_estimado = add_obvios(futuro_estimado)
    
    stop_counter = stop_counter +1
    if max_pilha < len(pilha):
      max_pilha = len(pilha)
    if log:
      display('Guess Pós iteracao:',pilha_guess[-1])
      print('Comprimento da pilha Sudoku = {}'.format(len(pilha)))
      print('-----------------------------------------------------------------------------------',stop_counter)
  fim = datetime.datetime.now()
  tempo_total = fim - inicio
  print(f'Tamanho maximo da pilha: {max_pilha}')
  print(f'Total de iteracoes necessarias: {stop_counter}')
  print(f'Tempo Total de Execucao: {str(tempo_total)[5:10]} segundos!')
  return pilha[-1],max_pilha,stop_counter,tempo_total

def create_sudoku():
  sudoku = [[' ' for x in range(1,10)] for x in range(1,10)]
  for i in range(0,9):
      n = input()
      n = list(n)
      for j, x in enumerate(n):
        if str(x) not in [str(y) for y in range(1,10)]:
          n[j] = ' '
        sudoku = insert_number(sudoku,i,j,n[j])
  return sudoku
  
  
def insert_number(matriz,linha,coluna,numero):
  sup = deepcopy(matriz)
  sup[linha][coluna] = numero
  return sup
  
def get_row(matriz, n):
  return matriz[n]
  
def get_column(matriz, n):
  coluna = []
  for linha in matriz:
    coluna.append(linha[n])
  return coluna
  
def get_square(matriz, n):
  square = []
  square_dict = {0:(0,0),1:(0,3),2:(0,6),
               3:(3,0),4:(3,3),5:(3,6),
               6:(6,0),7:(6,3),8:(6,6)}
  linha_base = square_dict[n][0]
  coluna_base = square_dict[n][1]
  for i in range(linha_base,linha_base+3,1):
    for j in range(coluna_base,coluna_base+3,1):
      square.append(matriz[i][j])
  return square
  
def get_square_number(linha,coluna):
  if linha <=2 and coluna <= 2:
    return 0
  elif linha <=2 and coluna <= 5:
    return 1
  elif linha <=2 and coluna <= 8:
    return 2
  elif linha <=5 and coluna <= 2:
    return 3
  elif linha <=5 and coluna <= 5:
    return 4
  elif linha <=5 and coluna <= 8:
    return 5
  elif linha <=8 and coluna <= 2:
    return 6
  elif linha <=8 and coluna <= 5:
    return 7
  elif linha <=8 and coluna <= 8:
    return 8
    
def check_no_repeated(lista):
  if any(lista.count(x) > 1 for x in lista if x != ' '):
    return False
  else:
    return True
    
def check_1to9(lista):
  if set([str(x) for x in range(1,10)]) == set(lista):
    return True
  else:
    return False
    
def check(matriz):
  #print('Validando Linhas...')
  for l in range(0,9):
    if check_no_repeated(get_row(matriz,l)) == False:
      return False
    if check_1to9(get_row(matriz,l)) == False:
      return False

  #print('Validando Colunas...')
  for c in range(0,9):
    if check_no_repeated(get_column(matriz, c)) == False:
      return False
    if check_1to9(get_column(matriz,c)) == False:
      return False

  #print('Validando Quadrados...')
  for s in range(0,9):
    if check_no_repeated(get_square(matriz, s)) == False:
      return False
    if check_1to9(get_square(matriz,s)) == False:
      return False

  print('Sudoku Completo!')
  return True
  
def missing_numbers(lista_linha,lista_coluna,lista_square):
  missing = [str(n) for n in range(1,10)]
  missing = [item for item in missing if item not in lista_linha]
  missing = [item for item in missing if item not in lista_coluna]
  missing = [item for item in missing if item not in lista_square]
  return missing
  
def create_pencil_matriz(matriz):
  sup_pencil = deepcopy(matriz)
  #display('sup pencil', sup_pencil)
  pencil_matriz = [[' ' for x in range(1,10)] for x in range(1,10)]
  for y,val_y in enumerate(pencil_matriz):
    for x, val_x in enumerate(range(0,9)):
      if sup_pencil[y][x] == ' ':
        pencil_matriz[y][x] = missing_numbers(get_row(sup_pencil,y),get_column(sup_pencil,x),get_square(sup_pencil,get_square_number(y,x)))
  return pencil_matriz
  
def insert_obvious(matriz):
  flag=0
  sup_obvious = deepcopy(matriz)
  pencil_matriz = create_pencil_matriz(sup_obvious)
  for i, linhas in enumerate(pencil_matriz):
    for j, colunas in enumerate(linhas):
      possibilidades = colunas
      if len(possibilidades) == 1 and possibilidades != ' ' and flag == 0:
        #print('Adding {} to Element {},{}'.format(possibilidades[0],i,j))
        sup_obvious = insert_number(sup_obvious, i,j,possibilidades[0])
        del possibilidades
        flag = 1
  return sup_obvious
      

def big_pencil_size(matriz):
  pencil_matriz = create_pencil_matriz(matriz)
  tamanhos = []
  for linhas in pencil_matriz:
    for valores in linhas:
      if valores != ' ':
        tamanhos.append(len(valores))
  print('MIN TAMANHOS:',min(tamanhos) )
  if min(tamanhos) >=2:
    return True
  else:
    return False 
    
def add_pilha(pilha, matriz, linha, coluna, n):
  matriz[linha][coluna] = n
  empilha(pilha,matriz)
  return pilha
  
def get_len_pencil(matriz):
  pencil = create_pencil_matriz(matriz)
  size_pencil = [[len(x) if x != ' ' else 0 for x in lista] for lista in pencil]
  return size_pencil

def get_ij_minimun_pencil(matriz):
  b = np.array(get_len_pencil(matriz))
  for n in range(2,10):
    onde = np.where(b==n)
    if onde[0].size != 0:
      i = onde[0][0]
      j = onde[1][0]
      return i,j
  return -1,-1
  
def insert_guess(matriz, guess_matriz,log=False):
  sup = deepcopy(matriz)
  guess_sup = deepcopy(guess_matriz)
  i,j = get_ij_minimun_pencil(sup)
  valores = create_pencil_matriz(sup)[i][j]
  if log:
    print('Trying to insert guess on {},{}'.format(i,j))
    print('Possiveis Valores: {}'.format(valores))
  sup,guess_sup = guess_maker(sup,valores,guess_sup,i,j)
  return i,j,sup,guess_sup
    
def guess_maker(matriz,valores,guess_matriz,i,j,log=False):
  sup_maker = deepcopy(matriz)
  guess_sup_maker = deepcopy(guess_matriz)
  valores = [x for x in valores if x not in guess_sup_maker[i][j]]

  guess_sup_maker[i][j].append(valores[0])
  guess = valores[0]
  sup_maker = insert_number(sup_maker,i,j,guess)
  if log:
    print('Adding GUESS {} to Element {},{}'.format(guess,i,j))
  return sup_maker, guess_sup_maker
  
def backtrack(matriz,guess_matriz,log=False):
  i,j = get_ij_minimun_pencil(matriz)
  print('Minimo i,j = {},{}'.format(i,j))
  valores = create_pencil_matriz(matriz)[i][j]
  valores = [x for x in valores if x not in guess_matriz[i][j]]
  if log:
    display('VALORES backtrack: ',valores)
  if len(valores) == 0:
    return True
  else:
    return False
    
def check_backtrack(matriz, guess_matriz,log=False):
  i,j = get_ij_minimun_pencil(matriz)
  if i == -1 and j == -1:
    return False
  if log:
    print('i,j para verificar no futuro: {}, {}'.format(i,j))
  valores = create_pencil_matriz(matriz)[i][j]
  valores = [x for x in valores if x not in guess_matriz[i][j]]
  if len(valores) == 0:
    return True
  else:
    return False

def add_obvios(matriz):
  sup = deepcopy(matriz)
  matriz = insert_obvious(matriz)
  while sup != matriz:
    sup = deepcopy(matriz)
    matriz = insert_obvious(sup)
  return matriz
  
def inicia_sudoku(matriz):
  sudoku = deepcopy(matriz)
  guess_sudoku = [[[] for i in range(9)] for i in range(9)]
  pilha = []
  pilha_guess = []
  pilha = empilha(pilha,sudoku) #pilha[-1] contem o mais correto
  pilha_guess = empilha(pilha_guess,guess_sudoku)
  flag=1
  return sudoku,pilha, guess_sudoku, pilha_guess, flag
  
def count_guess_vazios(guess_sudoku):
  count = 0
  for i in guess_sudoku:
    for j in i:
      if len(j) == 0:
        count = count+1
  return count
  
def empilha(pilha, matriz):
  sup = deepcopy(pilha)
  matriz_sup = deepcopy(matriz)
  sup.append(matriz_sup)
  return sup

def desempilha(pilha):
  sup = deepcopy(pilha)
  sup.pop()
  return sup
  
def small_pencil_size(matriz):
  pencil_matriz = deepcopy(create_pencil_matriz(matriz))
  tamanhos = []
  for linhas in pencil_matriz:
    for valores in linhas:
      if valores != ' ':
        tamanhos.append(len(valores))
  if tamanhos == []:
    return True
  if min(tamanhos) == 0:
    return True
  else:
    return False
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    