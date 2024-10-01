import tkinter as tk
from tkinter import ttk, scrolledtext
from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient('mongodb+srv://userclash:gmm2509@clashroyale.zisnx.mongodb.net/?retryWrites=true&w=majority&appName=ClashRoyale')
db = client['mydatabase']

# Função para ajustar a interface ao redimensionar
def ajustar_tela(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def aplicar_estilo(widget):
    try:
        widget.configure(bg='#1C75BC', fg='white', font=('Helvetica', 10, 'bold'))
    except tk.TclError:
        pass  # Ignora erros para widgets que não suportam fg ou bg

# Função para exibir os resultados formatados na área de texto
def exibir_resultados(resultados):
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END) 
    if resultados:
        for resultado in resultados:
            text_area.insert(tk.END, f"{resultado}\n\n")  
    else:
        text_area.insert(tk.END, "Nenhum resultado encontrado.\n\n") 
    text_area.config(state=tk.DISABLED)

# Funções de consulta
def calcular_porcentagem_vitorias():
    carta = "Bats"
    total_vitorias = db.batalha.count_documents({
        "deck_jogador1.nome": carta,
        "vencedor": "jogador1"
    }) + db.batalha.count_documents({
        "deck_jogador2.nome": carta,
        "vencedor": "jogador2"
    })
    total_derrotas = db.batalha.count_documents({
        "deck_jogador1.nome": carta,
        "vencedor": "jogador2"
    }) + db.batalha.count_documents({
        "deck_jogador2.nome": carta,
        "vencedor": "jogador1"
    })
    total_battles = total_vitorias + total_derrotas
    porcentagem_vitorias = (total_battles > 0) * (total_vitorias / total_battles * 100)
    porcentagem_derrotas = (total_battles > 0) * (total_derrotas / total_battles * 100)
    exibir_resultados([f"Porcentagem de Vitórias: {porcentagem_vitorias:.2f}%", 
                       f"Porcentagem de Derrotas: {porcentagem_derrotas:.2f}%"])


def listar_decks_porcentagem():
    porcentagem_minima = float(porcentagem_min_entry.get())
    porcentagem_maxima = float(porcentagem_max_entry.get())

    decks = db.batalha.aggregate([
        {
            '$project': {
                'deck_jogador1': '$deck_jogador1.nome',
                'vitorias_jogador1': {
                    '$cond': [{ '$eq': ["$vencedor", "jogador1"] }, 1, 0]
                }
            }
        },
        {
            '$group': {
                '_id': '$deck_jogador1',
                'totalVitorias': { '$sum': '$vitorias_jogador1' },
                'totalBatalhas': { '$sum': 1 }
            }
        },
        {
            '$project': {
                'deck': '$_id',
                'porcentagemVitorias': {
                    '$multiply': [{ '$divide': ['$totalVitorias', '$totalBatalhas'] }, 100]
                }
            }
        },
        {
            '$match': {
                'porcentagemVitorias': { '$gte': porcentagem_minima, '$lte': porcentagem_maxima }
            }
        }
    ])

    resultados = [f"Deck: {deck['deck']}, Porcentagem de Vitórias: {deck['porcentagemVitorias']:.2f}%" for deck in decks]
    exibir_resultados(resultados)


def calcular_derrotas_combo():
    combo = combo_entry.get().split(",") 
    total_derrotas_combo = db.batalha.count_documents({
        '$or': [
            { "deck_jogador1.nome": { '$all': combo }, "vencedor": "jogador2" },
            { "deck_jogador2.nome": { '$all': combo }, "vencedor": "jogador1" }
        ]
    })
    exibir_resultados([f"Total de derrotas usando o combo {', '.join(combo)}: {total_derrotas_combo}"])


def calcular_vitorias_com_carta():
    carta_x = carta_entry.get()
    min_trof = float(min_trof_entry.get())
    
    vitorias = db.batalha.aggregate([
        {
            '$match': {
                "deck_jogador1.nome": carta_x
            }
        },
        {
            '$group': {
                '_id': None,
                'vitorias': {
                    '$sum': {
                        '$cond': [{ '$eq': ["$vencedor", "jogador1"] }, 1, 0]
                    }
                },
                'totalBatalhas': { '$sum': 1 }
            }
        },
        {
            '$project': {
                'porcentagemVitorias': {
                    '$cond': [
                        { '$eq': ["$totalBatalhas", 0] },
                        0,
                        { '$multiply': [{ '$divide': ["$vitorias", "$totalBatalhas"] }, 100] }
                    ]
                },
                'derrotas': { '$subtract': ["$totalBatalhas", "$vitorias"] }
            }
        }
    ])
    
    resultado = next(v for v in vitorias)
    exibir_resultados([f"Porcentagem de Vitórias: {resultado['porcentagemVitorias']:.2f}%, Derrotas: {resultado['derrotas']}"])


def listar_combos_vitorias():
    tamanho_combo = int(tamanho_combo_entry.get())
    min_porcentagem = float(min_porcentagem_entry.get())

    combos = db.batalha.aggregate([
        {
            '$project': {
                'deck_jogador1': '$deck_jogador1.nome',
                'vitorias': {
                    '$cond': [{ '$eq': ["$vencedor", "jogador1"] }, 1, 0]
                }
            }
        },
        {
            '$group': {
                '_id': { '$slice': ["$deck_jogador1", tamanho_combo] },
                'totalVitorias': { '$sum': '$vitorias' },
                'totalBatalhas': { '$sum': 1 }
            }
        },
        {
            '$project': {
                'combo': '$_id',
                'porcentagemVitorias': { '$multiply': [{ '$divide': ["$totalVitorias", "$totalBatalhas"] }, 100] }
                }
        },
        {
            '$match': {
                'porcentagemVitorias': { '$gt': min_porcentagem }
            }
        }
    ])
    
    resultados = [f"Combo: {', '.join(combo['combo'])}, Porcentagem de Vitórias: {combo['porcentagemVitorias']:.2f}%" for combo in combos]
    exibir_resultados(resultados)


def cartas_maior_taxa_vitorias():
    cartas = db.batalha.aggregate([
        {
            '$unwind': "$deck_jogador1"
        },
        {
            '$group': {
                '_id': "$deck_jogador1.nome",
                'totalVitorias': {
                    '$sum': { '$cond': [{ '$eq': ["$vencedor", "jogador1"] }, 1, 0] }
                },
                'totalBatalhas': { '$sum': 1 }
            }
        },
        {
            '$project': {
                'porcentagemVitorias': { '$multiply': [{ '$divide': ["$totalVitorias", "$totalBatalhas"] }, 100] }
            }
        },
        {
            '$sort': { 'porcentagemVitorias': -1 }  # Ordenar em ordem decrescente
        },
        {
            '$limit': 5  # Limitar a 5 resultados
        }
    ])
    
    resultados = [f"Card: {carta['_id']}, Taxa de Vitórias: {carta['porcentagemVitorias']:.2f}%" for carta in cartas]
    exibir_resultados(resultados)


def top_3_combos_menor_taxa_vitoria():
    combos_menor_taxa = db.batalha.aggregate([
        {
            '$project': {
                'deck_jogador1': '$deck_jogador1.nome',  
                'vitorias_jogador1': {
                    '$cond': [{ '$eq': ["$vencedor", "jogador1"] }, 1, 0]
                }
            }
        },
        {
            '$group': {
                '_id': '$deck_jogador1',
                'totalVitorias': { '$sum': '$vitorias_jogador1' },
                'totalBatalhas': { '$sum': 1 }
            }
        },
        {
            '$project': {
                'combo': '$_id',
                'porcentagemVitorias': {
                    '$multiply': [{ '$divide': ['$totalVitorias', '$totalBatalhas'] }, 100]
                }
            }
        },
        {
            '$sort': { 'porcentagemVitorias': 1 }  # Ordena pela menor porcentagem de vitórias (ascendente)
        },
        {
            '$limit': 3  # Limita aos 3 combos com menor taxa de vitória
        }
    ])

    resultados = [f"Combo: {', '.join(combo['combo'])}, Taxa de Vitórias: {combo['porcentagemVitorias']:.2f}%" for combo in combos_menor_taxa]
    exibir_resultados(resultados)


def top10_cartas_mais_utilizadas():
    cartas_mais_utilizadas = db.batalha.aggregate([
        {
            '$unwind': '$deck_jogador1'
        },
        {
            '$group': {
                '_id': '$deck_jogador1.nome',
                'totalUsos': { '$sum': 1 }
            }
        },
        {
            '$sort': { 'totalUsos': -1 }
        },
        {
            '$limit': 10
        }
    ])

    resultados = [f"Carta: {carta['_id']}, Utilizações: {carta['totalUsos']}" for carta in cartas_mais_utilizadas]
    exibir_resultados(resultados)


# Interface
janela = tk.Tk()
janela.title("Clash Royale Querys")
janela.geometry("700x600")
janela.configure(bg='#1C75BC')

canvas = tk.Canvas(janela)
scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Rótulos e entradas grid (horizontal)
lbl_porcentagem_min = tk.Label(scrollable_frame, text="Porcentagem mínima de vitórias:")
porcentagem_min_entry = tk.Entry(scrollable_frame)

lbl_porcentagem_max = tk.Label(scrollable_frame, text="Porcentagem máxima de vitórias:")
porcentagem_max_entry = tk.Entry(scrollable_frame)

lbl_combo = tk.Label(scrollable_frame, text="Cartas do combo (separadas por vírgula):")
combo_entry = tk.Entry(scrollable_frame)

lbl_carta = tk.Label(scrollable_frame, text="Nome da carta:")
carta_entry = tk.Entry(scrollable_frame)

lbl_min_trof = tk.Label(scrollable_frame, text="Diferença mínima de troféus (%):")
min_trof_entry = tk.Entry(scrollable_frame)

lbl_tamanho_combo = tk.Label(scrollable_frame, text="Tamanho do combo:")
tamanho_combo_entry = tk.Entry(scrollable_frame)

lbl_min_porcentagem = tk.Label(scrollable_frame, text="Porcentagem mínima de vitórias:")
min_porcentagem_entry = tk.Entry(scrollable_frame)

# Botons
btn_porcentagem_vitorias = tk.Button(scrollable_frame, text="Porcentagem de Vitórias", command=calcular_porcentagem_vitorias)
btn_listar_decks = tk.Button(scrollable_frame, text="Listar Decks com Porcentagem de Vitórias", command=listar_decks_porcentagem)
btn_calcular_derrotas_combo = tk.Button(scrollable_frame, text="Derrotas por Combo(x)", command=calcular_derrotas_combo)
btn_calcular_vitorias = tk.Button(scrollable_frame, text="Vitórias por Carta", command=calcular_vitorias_com_carta)
btn_listar_combos_vitorias = tk.Button(scrollable_frame, text="Listar Combos com Porcentagem de Vitórias", command=listar_combos_vitorias)
btn_cartas_maior_taxa_vitorias = tk.Button(scrollable_frame, text="Top 5 carta/Vitórias", command=cartas_maior_taxa_vitorias)
btn_menor_taxa_vitoria = tk.Button(scrollable_frame, text="Top 3 Combos Menor Taxa de Vitória", command=top_3_combos_menor_taxa_vitoria)
btn_top10_cartas_utilizadas = tk.Button(scrollable_frame, text="Top 10 Cartas Utilizadas", command=top10_cartas_mais_utilizadas)

# Rótulos e entradas grid (posições)
lbl_porcentagem_min.grid(row=0, column=0, padx=5, pady=5, sticky='e')
porcentagem_min_entry.grid(row=0, column=1, padx=5, pady=5)

lbl_porcentagem_max.grid(row=1, column=0, padx=5, pady=5, sticky='e')
porcentagem_max_entry.grid(row=1, column=1, padx=5, pady=5)

lbl_combo.grid(row=2, column=0, padx=5, pady=5, sticky='e')
combo_entry.grid(row=2, column=1, padx=5, pady=5)

lbl_carta.grid(row=3, column=0, padx=5, pady=5, sticky='e')
carta_entry.grid(row=3, column=1, padx=5, pady=5)

lbl_min_trof.grid(row=4, column=0, padx=5, pady=5, sticky='e')
min_trof_entry.grid(row=4, column=1, padx=5, pady=5)

lbl_tamanho_combo.grid(row=5, column=0, padx=5, pady=5, sticky='e')
tamanho_combo_entry.grid(row=5, column=1, padx=5, pady=5)

lbl_min_porcentagem.grid(row=6, column=0, padx=5, pady=5, sticky='e')
min_porcentagem_entry.grid(row=6, column=1, padx=5, pady=5)

# Posicionando botões
btn_porcentagem_vitorias.grid(row=7, column=0, columnspan=1, pady=5)
btn_listar_decks.grid(row=8, column=0, columnspan=1, pady=5)
btn_calcular_derrotas_combo.grid(row=9, column=0, columnspan=1, pady=5)
btn_calcular_vitorias.grid(row=10, column=0, columnspan=1, pady=5)
btn_listar_combos_vitorias.grid(row=11, column=0, columnspan=1, pady=5)
btn_cartas_maior_taxa_vitorias.grid(row=7, column=1, columnspan=1, pady=5)
btn_menor_taxa_vitoria.grid(row=8, column=1, columnspan=1, pady=5)
btn_top10_cartas_utilizadas.grid(row=9, column=1, columnspan=1, pady=5)

# Área de texto (Resultados)
text_area = scrolledtext.ScrolledText(scrollable_frame, wrap=tk.WORD, height=10)
text_area.grid(row=12, column=0, columnspan=2, padx=10, pady=10)
text_area.config(state=tk.DISABLED)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

janela.mainloop()
