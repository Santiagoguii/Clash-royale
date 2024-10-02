# Clash Royale API**

## **🚀Objetivo do Projeto:**
Armazenar dados de batalhas do jogo em um BD NoSQLpara viabilizar consultas analíticas que permitamanalisar estatísticas de vitórias/derrotas associadas ao
uso das cartas, visando balancear o jogo.

## **📑Pré-requisitos:**
Para rodar o software é necessário ter o python 3.7 para cima, e instalar e importar algumas bibliotecas com os comandos descritos abaixo.

```
#instalar biblioteca 
pip install tk
pip install pymongo

#importar biblioteca
import tkinter as tk
from pymongo import MongoClient
from tkinter import *
```

## **📋Consultas:**
1. Calcule a porcentagem de vitórias e derrotas utilizando a carta X(parâmetro) ocorridas em um intervalo de timestamps (parâmetro).
2. Liste os decks completos que produziram mais de X% (parâmetro) de vitórias ocorridas em um intervalo de timestamps (parâmetro).
3. Calcule a quantidade de derrotas utilizando o combo de cartas(X1,X2, ...) (parâmetro) ocorridas em um intervalo de timestamps (parâmetro).
4. Calcule a quantidade de vitórias envolvendo a carta X (parâmetro) nos casos em que o vencedor possui Z% (parâmetro) menos troféus do que o perdedor, a partida durou menos de 2 minutos, e o perdedor derrubou ao menos duas torres do adversário.
5. Liste o combo de cartas (eg: carta 1, carta 2, carta 3... carta n) de tamanho N (parâmetro) que produziram mais de Y% (parâmetro) de vitórias ocorridas em um intervalo de timestamps (parâmetros).
6. Elabore mais 3 consultas que você julga relevante para auxiliar no balanceamento do jogo.

## **🃏 Funcionalidades e parâmetros:**

### 1. Porcentagem de Vitórias:
- Botão: `Porcentagem de Vitórias`
- Descrição: Calcula a porcentagem de vitórias e derrotas de uma carta específica.
- Parâmetros Necessários:
  - Nenhum parâmetro adicional é necessário. A carta está hardcoded como "Bats".

### 2. Listar Decks com Porcentagem de Vitórias
- Botão: `Listar Decks com Porcentagem de Vitórias`
- Descrição: Lista os decks que possuem uma porcentagem de vitórias dentro de um intervalo definido pelo usuário.
- Parâmetros Necessários: 
  - Porcentagem mínima de vitórias: Insira o valor mínimo desejado (por exemplo, 50).
  - Porcentagem máxima de vitórias: Insira o valor máximo desejado (por exemplo, 70).

### 3. Derrotas por Combo:
- Botão: `Derrotas por Combo`
- Descrição: Conta quantas derrotas ocorreram usando um combo específico de cartas.
- Parâmetros Necessários: 
  - Nenhum parâmetro adicional é necessário. O combo está hardcoded como ["Mortar", "Bats", "Miner", "Skeleton King", "Cannon Cart", "Goblin Gang", "Ice Wizard", "Arrows"].

### 4. Vitórias por Carta:
- Botão: `Vitórias por Carta`
- Descrição: Calcula a porcentagem de vitórias de uma carta específica em relação às suas batalhas e exibe também o número de derrotas.
- Parâmetros Necessários:
  - Nome da carta: Insira o nome da carta (por exemplo, Fireball).
  - Diferença mínima de troféus (%): Insira o valor mínimo de troféus (por exemplo, 5).

### 5. Listar Combos com Porcentagem de Vitórias:
- Botão: `Listar Combos com Porcentagem de Vitórias`
- Descrição: Lista combos de cartas que possuem uma porcentagem de vitórias acima de um determinado valor.
- Parâmetros Necessários:
  - Tamanho do combo: Insira o número de cartas no combo (por exemplo, 3).
  - Porcentagem mínima de vitórias: Insira a porcentagem mínima (por exemplo, 55).

### 6. Top 5 Cartas com Maior Taxa de Vitórias:
- Botão: `Top 5 carta/Vitórias`
- Descrição: Exibe as 5 cartas que possuem a maior taxa de vitórias.
- Parâmetros Necessários: 
  - Nenhum parâmetro adicional é necessário.

### 7. Top 3 Combos com Menor Taxa de Vitória:
- Botão: `Top 3 Combos Menor Taxa de Vitória`
- Descrição: Exibe os 3 combos que possuem a menor taxa de vitória.
- Parâmetros Necessários:
  - Nenhum parâmetro adicional é necessário.

### 8. Top 10 Cartas Mais Utilizadas:
- Botão: `Top 10 Cartas Utilizadas`
- Descrição: Lista as 10 cartas que foram mais utilizadas nas batalhas.
- Parâmetros Necessários: 
  - Nenhum parâmetro adicional é necessário.


## **🛠️Construído com:**
[Python](https://docs.python.org/pt-br/3/tutorial/) - linguaguem utilizada
[Tkinter](https://www.tkdocs.com/tutorial/index.html) - Interface gráfica do usuário

## **✒️ Autores:**
Guilherme Santiago* - Desenvolvedor - [github](https://github.com/santiagoguii)
Mateus Caik* - Desenvolvedor - [github](https://github.com/mateuscaik)
Micaelle Silva - Desenvolvedora - [github](https://github.com/micaellesilvaa)
