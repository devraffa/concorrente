# jogo.py

tabuleiro = [' '] * 9 

def imprimir_tabuleiro():
    print(f"\n{tabuleiro[0]} | {tabuleiro[1]} | {tabuleiro[2]}")
    print("--+---+--")
    print(f"{tabuleiro[3]} | {tabuleiro[4]} | {tabuleiro[5]}")
    print("--+---+--")
    print(f"{tabuleiro[6]} | {tabuleiro[7]} | {tabuleiro[8]}")
    print("\n")


def verificar_vitoria():
    vitoria_possibilidades = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6] 
    ]
    
    for pos in vitoria_possibilidades:
        if tabuleiro[pos[0]] == tabuleiro[pos[1]] == tabuleiro[pos[2]] != ' ':
            return tabuleiro[pos[0]] 
    if ' ' not in tabuleiro: 
        return 'Empate'
    return None