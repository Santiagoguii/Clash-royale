#**Clash Royale API**

📑 **Objetivo do Projeto**
Armazenar dados de batalhas do jogo em um BD NoSQLpara viabilizar consultas analíticas que permitamanalisar estatísticas de vitórias/derrotas associadas ao
uso das cartas, visando balancear o jogo

📋**Consultas:**
1. Calcule a porcentagem de vitórias e derrotas utilizando a carta X(parâmetro) ocorridas em um intervalo de timestamps (parâmetro).
2. Liste os decks completos que produziram mais de X% (parâmetro) de vitórias ocorridas em um intervalo de timestamps (parâmetro).
3. Calcule a quantidade de derrotas utilizando o combo de cartas(X1,X2, ...) (parâmetro) ocorridas em um intervalo de timestamps (parâmetro).
4. Calcule a quantidade de vitórias envolvendo a carta X (parâmetro) nos casos em que o vencedor possui Z% (parâmetro) menos troféus do que o perdedor, a partida durou menos de 2 minutos, e o perdedor derrubou ao menos duas torres do adversário.
5. Liste o combo de cartas (eg: carta 1, carta 2, carta 3... carta n) de tamanho N (parâmetro) que produziram mais de Y% (parâmetro) de vitórias ocorridas em um intervalo de timestamps (parâmetros).
6. Elabore mais 3 consultas que você julga relevante para auxiliar no balanceamento do jogo.

📋 **Pré-requisitos**
Para rodar o software é necessário ter o python 3.7 para cima, e instalar e importar algumas bibliotecas com os comandos descritos abaixo.

#instalar biblioteca 
pip install tk
pip install pymongo

#importar biblioteca
import tkinter as tk
from pymongo import MongoClient
from tkinter import *

🛠️ **Construído com**
[Python](https://docs.python.org/pt-br/3/tutorial/) - linguaguem utilizada
[Tkinter](https://www.tkdocs.com/tutorial/index.html) - Interface gráfica do usuário

✒️ **Autores**
Guilherme Santiago* - Desenvolvedor - [github](https://github.com/santiagoguii)
Mateus Caik* - Desenvolvedor - [github](https://github.com/mateuscaik)
Micaelle Silva - Desenvolvedora - [github](https://github.com/micaellesilvaa)
