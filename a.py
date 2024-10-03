import tkinter as tk
from tkinter import messagebox
import requests
import mongoengine as me

API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImU3ZWEyODZkLTI1OGQtNGQwNS04ZGRiLWUzYjA1MThmMDc3ZiIsImlhdCI6MTcyNzU0NzY4NSwic3ViIjoiZGV2ZWxvcGVyL2NjYjExYWI1LTMxYjMtY2E1Yy0wMzZkLWExYzQ4MTkzMzNmNiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIyMDEuNTkuMTY5LjkiXSwidHlwZSI6ImNsaWVudCJ9XX0.vM15ZpYLpcO407axS1j-BlbQcEhddKUahf_EGyNfkqwuBkaT2Y1HphaaPmU9nRx2BH5ikaJFZkB9Xiw97NqIvQ'
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# Conectar ao MongoDB
me.connect('clash_royale_db', host='localhost', port=27017)

# Definir modelo de dados para jogador
class Jogador(me.Document):
    player_id = me.StringField(required=True)
    nickname = me.StringField(required=True)
    trofeus = me.IntField()
    nivel = me.IntField()
    total_vitorias = me.IntField()
    total_derrotas = me.IntField()

# Definir modelo de dados para batalhas
class Batalha(me.Document):
    player_id = me.StringField(required=True)
    batalha_id = me.StringField(required=True)
    vencedor = me.StringField(required=True)
    trofeus_ganhos = me.IntField()
    trofeus_perdidos = me.IntField()
    cartas = me.ListField(me.StringField())

# Função para obter dados de um jogador
def get_player_info(player_tag):
    url = f"https://api.clashroyale.com/v1/players/%23{player_tag.upper()}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Erro", f"Erro {response.status_code}: {response.text}")
        return None

# Função para obter batalhas de um jogador
def get_player_battles(player_tag):
    url = f"https://api.clashroyale.com/v1/players/%23{player_tag.upper()}/battlelog"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Erro", f"Erro {response.status_code}: {response.text}")
        return None

# Função para salvar jogador no MongoDB
def salvar_jogador_no_mongodb(player_data):
    jogador = Jogador(
        player_id=player_data['tag'],
        nickname=player_data['name'],
        trofeus=player_data['trophies'],
        nivel=player_data['expLevel'],
        total_vitorias=player_data['wins'],
        total_derrotas=player_data['losses']
    )
    jogador.save()

# Função para salvar batalhas no MongoDB
def salvar_batalhas_no_mongodb(player_tag, batalhas):
    for batalha in batalhas:
        batalha_doc = Batalha(
            player_id=player_tag,
            batalha_id=batalha['battleTime'],  # Usando battleTime como ID único
            vencedor=batalha['team'][0]['name'] if batalha['team'][0]['crowns'] > batalha['opponent'][0]['crowns'] else batalha['opponent'][0]['name'],
            trofeus_ganhos=batalha['team'][0]['trophyChange'] if batalha['team'][0]['crowns'] > batalha['opponent'][0]['crowns'] else 0,
            trofeus_perdidos=batalha['opponent'][0]['trophyChange'] if batalha['opponent'][0]['crowns'] > batalha['team'][0]['crowns'] else 0,
            cartas=[carta['name'] for carta in batalha['team'][0]['cards']]
        )
        batalha_doc.save()

# Função acionada pelo botão "Buscar"
def buscar_jogador():
    player_tag = entry_player_tag.get()
    if player_tag:
        # Buscar e salvar jogador
        player_info = get_player_info(player_tag)
        if player_info:
            salvar_jogador_no_mongodb(player_info)
            messagebox.showinfo("Sucesso", "Jogador salvo com sucesso")
        
        # Buscar e salvar batalhas
        player_battles = get_player_battles(player_tag)
        if player_battles:
            salvar_batalhas_no_mongodb(player_tag, player_battles)
            messagebox.showinfo("Sucesso", "Batalhas salvas com sucesso")
    else:
        messagebox.showwarning("Atenção", "Por favor, insira uma tag de jogador.")

# Criar interface gráfica
root = tk.Tk()
root.title("Buscar Jogador e Salvar no MongoDB")
root.geometry("400x200")

# Campo para inserir a tag do jogador
label_player_tag = tk.Label(root, text="Tag do Jogador:")
label_player_tag.pack(pady=10)
entry_player_tag = tk.Entry(root)
entry_player_tag.pack(pady=10)

# Botão para buscar o jogador
btn_buscar = tk.Button(root, text="Buscar", command=buscar_jogador)
btn_buscar.pack(pady=10)

# Rodar a interface
root.mainloop()
    