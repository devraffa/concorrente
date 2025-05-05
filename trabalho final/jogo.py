class JogoDaVela:
    def __init__(self):
        self.tabuleiro = {
            '7': ' ', '8': ' ', '9': ' ',
            '4': ' ', '5': ' ', '6': ' ',
            '1': ' ', '2': ' ', '3': ' '
        }

    def exibir_tabuleiro(self):
        return (
            f"┌───┬───┬───┐\n"
            f"│ {self.tabuleiro['7']} │ {self.tabuleiro['8']} │ {self.tabuleiro['9']} │\n"
            f"├───┼───┼───┤\n"
            f"│ {self.tabuleiro['4']} │ {self.tabuleiro['5']} │ {self.tabuleiro['6']} │\n"
            f"├───┼───┼───┤\n"
            f"│ {self.tabuleiro['1']} │ {self.tabuleiro['2']} │ {self.tabuleiro['3']} │\n"
            f"└───┴───┴───┘\n"
        )

    def verificar_vitoria(self):
        comb = [
            ('7', '8', '9'), ('4', '5', '6'), ('1', '2', '3'),
            ('7', '4', '1'), ('8', '5', '2'), ('9', '6', '3'),
            ('7', '5', '3'), ('1', '5', '9')
        ]
        for a, b, c in comb:
            if self.tabuleiro[a] == self.tabuleiro[b] == self.tabuleiro[c] != ' ':
                return self.tabuleiro[a]
        if ' ' not in self.tabuleiro.values():
            return 'empate'
        return None

    def fazer_jogada(self, pos, jogador):
        if pos in self.tabuleiro and self.tabuleiro[pos] == ' ':
            self.tabuleiro[pos] = jogador
            return True
        return False

    def get_tabuleiro(self):
        return self.tabuleiro
