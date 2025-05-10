## servidor.py
import socket
import threading
from sala import Sala

class Servidor:
    def __init__(self):
        self.fila_espera = []  # (conn, nome)
        self.fila_lock = threading.Lock()
        self.salas_ativas = {}
        self.sala_id_counter = 0

    def remover_sala(self, id_sala):
        if id_sala in self.salas_ativas:
            del self.salas_ativas[id_sala]
            print(f"[SERVIDOR] Sala {id_sala} encerrada.")

    def reenfileirar(self, jogador, nome):
        with self.fila_lock:
            self.fila_espera.append((jogador, nome))
            print(f"[SERVIDOR] Jogador '{nome}' retornou à fila.")
            if len(self.fila_espera) >= 2:
                self.iniciar_nova_sala()

    def iniciar_nova_sala(self):
        (jogador1, nome1) = self.fila_espera.pop(0)
        (jogador2, nome2) = self.fila_espera.pop(0)
        sala_id = self.sala_id_counter
        self.sala_id_counter += 1
        print(f"[SERVIDOR] Criando sala {sala_id} entre {nome1} e {nome2}.")
        sala = Sala(jogador1, jogador2, nome1, nome2, self, sala_id)
        self.salas_ativas[sala_id] = sala
        sala.iniciar()

    def lidar_com_cliente(self, conn, addr):
        print(f"[INFO] Novo jogador conectado: {addr}")
        try:
            nome = conn.recv(1024).decode().strip()
            print(f"[INFO] Jogador '{nome}' registrado.")
        except:
            print(f"[ERRO] Falha ao receber nome de {addr}")
            conn.close()
            return

        with self.fila_lock:
            self.fila_espera.append((conn, nome))
            if len(self.fila_espera) >= 2:
                self.iniciar_nova_sala()

    def iniciar(self, host='localhost', porta=12345):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((host, porta))
        servidor.listen()
        print(f"[SERVIDOR] Iniciado em {host}:{porta}")

        while True:
            conn, addr = servidor.accept()
            threading.Thread(target=self.lidar_com_cliente, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    Servidor().iniciar()
