import threading
from jogo import JogoDaVela

class Sala:
    def __init__(self, jogador1, jogador2):
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.jogo = JogoDaVela()
        self.turno = 'X'  # Começa com jogador1 sendo 'X'
        self.jogadores = {'X': jogador1, 'O': jogador2}
        self.simbolos = {jogador1: 'X', jogador2: 'O'}

        threading.Thread(target=self.rodar_jogo).start()

    def enviar_tabuleiro(self):
        estado = self.jogo.exibir_tabuleiro()
        try:
            self.jogador1.sendall(estado.encode())
            self.jogador2.sendall(estado.encode())
        except:
            print("Erro ao enviar tabuleiro.")

    def rodar_jogo(self):
        while True:
            self.enviar_tabuleiro()
            atual = self.jogadores[self.turno]

            try:
                atual.sendall(f"Sua vez ({self.turno}): ".encode())
                jogada = atual.recv(1024).decode().strip()
            except:
                print("Erro ao receber jogada.")
                break

            if not self.jogo.fazer_jogada(jogada, self.turno):
                atual.sendall("Jogada inválida. Tente novamente.\n".encode())
                continue

            vencedor = self.jogo.verificar_vitoria()
            if vencedor:
                self.enviar_tabuleiro()
                if vencedor == 'empate':
                    self.jogador1.sendall("Empate!\n".encode())
                    self.jogador2.sendall("Empate!\n".encode())
                else:
                    ganhador = self.jogadores[vencedor]
                    perdedor = self.jogador1 if ganhador == self.jogador2 else self.jogador2
                    ganhador.sendall("Você venceu!\n".encode())
                    perdedor.sendall("Você perdeu!\n".encode())
                break

            # Troca o turno
            self.turno = 'O' if self.turno == 'X' else 'X'

        # Encerra a partida
        try:
            self.jogador1.close()
            self.jogador2.close()
        except:
            pass
