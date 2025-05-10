## servidor.py
import socket
import threading
from sala import Sala

class Servidor:
    def __init__(self):
        self.fila_espera = []
        self.fila_lock = threading.Lock()
        self.salas_ativas = {}
        self.sala_id_counter = 0

    def remover_sala(self, id_sala):
        if id_sala in self.salas_ativas:
            del self.salas_ativas[id_sala]
            print(f"[SERVIDOR] Sala {id_sala} encerrada.")

    def reenfileirar(self, jogador):
        with self.fila_lock:
            self.fila_espera.append(jogador)
            print("[SERVIDOR] Jogador retornou à fila.")
            if len(self.fila_espera) >= 2:
                self.iniciar_nova_sala()

    def iniciar_nova_sala(self):
        jogador1 = self.fila_espera.pop(0)
        jogador2 = self.fila_espera.pop(0)
        sala_id = self.sala_id_counter
        self.sala_id_counter += 1
        print(f"[SERVIDOR] Criando sala {sala_id} entre dois jogadores.")
        sala = Sala(jogador1, jogador2, self, sala_id)
        self.salas_ativas[sala_id] = sala
        sala.iniciar()

    def lidar_com_cliente(self, conn, addr):
        print(f"[INFO] Novo jogador conectado: {addr}")
        try:
            conn.sendall(b"Conectado ao servidor!\nAguardando outro jogador...\n")
        except:
            print(f"[ERRO] Falha ao enviar mensagem para {addr}")
            conn.close()
            return

        with self.fila_lock:
            self.fila_espera.append(conn)
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
