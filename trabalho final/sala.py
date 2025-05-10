# sala.py
import threading
from jogo import JogoDaVela
import socket
import time

class Sala:
    def __init__(self, jogador1, jogador2):
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.lock = threading.Lock()

    def iniciar(self):
        threading.Thread(target=self.rodar_partidas, daemon=True).start()

    def rodar_partidas(self):
        continuar = True
        while continuar:
            self.jogo = JogoDaVela()
            self.turno = 'X'
            self.jogadores = {'X': self.jogador1, 'O': self.jogador2}
            self.simbolos = {self.jogador1: 'X', self.jogador2: 'O'}

            partida_ativa = True
            while partida_ativa:
                self.enviar_tabuleiro()
                atual = self.jogadores[self.turno]
                outro = self.jogador1 if atual == self.jogador2 else self.jogador2

                try:
                    #atual.sendall(f"Sua vez ({self.turno}): ".encode())
                    atual.sendall(f"Sua vez ({self.turno}): \n".encode())

                    jogada = atual.recv(1024).decode().strip()
                except:
                    outro.sendall("O outro jogador caiu. Encerrando.\n".encode())
                    outro.close()
                    return

                if jogada.upper() == "SAIR":
                    atual.sendall("Você encerrou a partida.\n".encode())
                    outro.sendall("O outro jogador saiu. Encerrando.\n".encode())
                    outro.close()
                    atual.close()
                    return

                if not self.jogo.fazer_jogada(jogada, self.turno):
                    atual.sendall("Jogada inválida. Tente novamente.\n".encode())
                    continue

                vencedor = self.jogo.verificar_vitoria()
                if vencedor:
                    self.enviar_tabuleiro()
                    if vencedor == 'empate':
                        self.broadcast("Empate!\n")
                    else:
                        self.jogadores[vencedor].sendall("Você venceu!\n".encode())
                        perdedor = self.jogador1 if self.jogadores[vencedor] == self.jogador2 else self.jogador2
                        perdedor.sendall("Você perdeu!\n".encode())
                    partida_ativa = False
                else:
                    self.turno = 'O' if self.turno == 'X' else 'X'

            continuar = self.perguntar_nova_partida()
            
        return False
            
    def enviar_tabuleiro(self):
        estado = self.jogo.exibir_tabuleiro()
        self.broadcast(estado)

    def broadcast(self, mensagem):
        try:
            self.jogador1.sendall(mensagem.encode())
            self.jogador2.sendall(mensagem.encode())
        except:
            pass

    def perguntar_nova_partida(self):
        try:
            self.jogador1.sendall(b"Deseja jogar novamente? (SIM/NAO): ")
            self.jogador2.sendall(b"Deseja jogar novamente? (SIM/NAO): ")

            resp1 = self.jogador1.recv(1024).decode().strip().upper()
            resp2 = self.jogador2.recv(1024).decode().strip().upper()

            if resp1 == "SAIR":
                self.jogador2.sendall(b"O outro jogador saiu. Encerrando...\n")
                return False
            if resp2 == "SAIR":
                self.jogador1.sendall(b"O outro jogador saiu. Encerrando...\n")
                return False

            if resp1 == "SIM" and resp2 == "SIM":
                self.broadcast("Iniciando nova partida!\n")
                return True
            elif resp1 == "SIM":
                self.jogador1.sendall("Aguardando novo jogador...\n".encode())
                self.jogador2.sendall("Você saiu do jogo.\n".encode())
                self.jogador2.close()
                return False
            elif resp2 == "SIM":
                self.jogador2.sendall("Aguardando novo jogador...\n".encode())
                self.jogador1.sendall("Você saiu do jogo.\n".encode())
                self.jogador1.close()
                return False
            else:
                self.broadcast("Encerrando conexão. Obrigado por jogar!\n")
                self.jogador1.close()
                self.jogador2.close()
                return False
        except:
            return False
