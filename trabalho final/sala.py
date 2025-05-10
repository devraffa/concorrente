
## sala.py
import threading
import socket
import time
from jogo import JogoDaVela

class Sala:
    def __init__(self, jogador1, jogador2, nome1, nome2, servidor, id_sala):
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.nome1 = nome1
        self.nome2 = nome2
        self.servidor = servidor
        self.id_sala = id_sala
        self.trocar_ordem = False

    def iniciar(self):
        threading.Thread(target=self.rodar_partidas, daemon=True).start()

    def rodar_partidas(self):
        continuar = True
        while continuar:
            self.jogo = JogoDaVela()
            if self.trocar_ordem:
                self.jogadores = {'X': self.jogador2, 'O': self.jogador1}
                nomes = {'X': self.nome2, 'O': self.nome1}
            else:
                self.jogadores = {'X': self.jogador1, 'O': self.jogador2}
                nomes = {'X': self.nome1, 'O': self.nome2}
            self.turno = 'X'

            self.broadcast(f"Partida entre {nomes['X']} (X) e {nomes['O']} (O). Boa sorte!\n")

            partida_ativa = True
            while partida_ativa:
                self.enviar_tabuleiro()
                atual = self.jogadores[self.turno]
                outro = self.jogadores['O' if self.turno == 'X' else 'X']

                try:
                    atual.sendall(f"Sua vez ({self.turno}):\n".encode())

                    while True:
                        jogada = atual.recv(1024).decode().strip()
                        if jogada.upper() == "SAIR":
                            atual.sendall("DESCONECTADO\n".encode())
                            outro.sendall("[AVISO] O outro jogador saiu. Você voltará à fila.\n")
                            time.sleep(1)
                            self.servidor.reenfileirar(outro, self.nome1 if atual == self.jogador2 else self.nome2)
                            atual.shutdown(socket.SHUT_RDWR)
                            atual.close()
                            self.servidor.remover_sala(self.id_sala)
                            return
                        elif jogada in [str(i) for i in range(1, 10)] and self.jogo.fazer_jogada(jogada, self.turno):
                            break
                        else:
                            atual.sendall("[AVISO] Entrada inválida ou não é sua vez.\n".encode())

                except:
                    outro.sendall("[AVISO] O outro jogador caiu. Você voltará à fila.\n".encode())
                    time.sleep(1)
                    self.servidor.reenfileirar(outro, self.nome2 if atual == self.jogador2 else self.nome1)
                    self.servidor.remover_sala(self.id_sala)
                    return

                vencedor = self.jogo.verificar_vitoria()
                if vencedor:
                    self.enviar_tabuleiro()
                    if vencedor == 'empate':
                        self.broadcast("Empate!\n")
                    else:
                        ganhador = self.jogadores[vencedor]
                        ganhador.sendall("Você venceu!\n".encode())
                        outro.sendall("Você perdeu!\n".encode())
                    partida_ativa = False
                else:
                    self.turno = 'O' if self.turno == 'X' else 'X'

            continuar = self.perguntar_nova_partida()
            self.trocar_ordem = not self.trocar_ordem

        self.servidor.remover_sala(self.id_sala)

    def enviar_tabuleiro(self):
        estado = self.jogo.exibir_tabuleiro()
        self.broadcast(estado)

    def broadcast(self, mensagem):
        for sock in (self.jogador1, self.jogador2):
            try:
                sock.sendall(mensagem.encode())
            except:
                pass

    def perguntar_nova_partida(self):
        try:
            self.jogador1.sendall(b"Deseja jogar novamente? (SIM/SAIR): ")
            self.jogador2.sendall(b"Deseja jogar novamente? (SIM/SAIR): ")

            resp1 = self.jogador1.recv(1024).decode().strip().upper()
            resp2 = self.jogador2.recv(1024).decode().strip().upper()

            if resp1 == "SAIR":
                self.jogador1.sendall(b"DESCONECTADO\n")
                self.jogador2.sendall(b"O outro jogador saiu. Voce voltara a fila.\n")
                self.servidor.reenfileirar(self.jogador2, self.nome2)
                return False
            if resp2 == "SAIR":
                self.jogador2.sendall(b"DESCONECTADO\n")
                self.jogador1.sendall(b"O outro jogador saiu. Voce voltara a fila.\n")
                self.servidor.reenfileirar(self.jogador1, self.nome1)
                return False

            if resp1 == "SIM" and resp2 == "SIM":
                self.broadcast("Iniciando nova partida!\n")
                return True
            elif resp1 == "SIM":
                self.jogador1.sendall(b"Voce voltou para a fila.\n")
                self.jogador2.sendall(b"Voce saiu do jogo. Encerrando...\n")
                self.servidor.reenfileirar(self.jogador1, self.nome1)
                self.jogador2.close()
                return False
            elif resp2 == "SIM":
                self.jogador2.sendall(b"Voce voltou para a fila.\n")
                self.jogador1.sendall(b"Voce saiu do jogo. Encerrando...\n")
                self.servidor.reenfileirar(self.jogador2, self.nome2)
                self.jogador1.close()
                return False
            else:
                self.broadcast("Encerrando conexão. Obrigado por jogar!\n")
                self.jogador1.close()
                self.jogador2.close()
                return False
        except:
            return False
