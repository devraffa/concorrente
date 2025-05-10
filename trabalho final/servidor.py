## servidor.py
import socket
import threading
import time
from sala import Sala

class Servidor:
    def __init__(self):
        self.fila_espera = []  # (conn, nome, timestamp)
        self.fila_lock = threading.Lock()
        self.salas_ativas = {}
        self.sala_id_counter = 0
        self.medidas = {
            "inicio_fila": {},
            "tempo_em_fila": [],
            "tempo_partidas": [],
            "salas_criadas": 0
        }
        self.rodando = True

    def remover_sala(self, id_sala):
        if id_sala in self.salas_ativas:
            inicio = self.salas_ativas[id_sala]['inicio']
            duracao = time.time() - inicio
            self.medidas['tempo_partidas'].append(duracao)
            print(f"[SERVIDOR] Sala {id_sala} encerrada. Duração: {duracao:.2f} segundos.")
            del self.salas_ativas[id_sala]

    def reenfileirar(self, jogador, nome):
        with self.fila_lock:
            self.fila_espera.append((jogador, nome, time.time()))
            print(f"[SERVIDOR] Jogador '{nome}' retornou à fila.")
            if len(self.fila_espera) >= 2:
                self.iniciar_nova_sala()

    def iniciar_nova_sala(self):
        (jogador1, nome1, t1) = self.fila_espera.pop(0)
        (jogador2, nome2, t2) = self.fila_espera.pop(0)
        agora = time.time()
        self.medidas['tempo_em_fila'].append(agora - t1)
        self.medidas['tempo_em_fila'].append(agora - t2)
        sala_id = self.sala_id_counter
        self.sala_id_counter += 1
        print(f"[SERVIDOR] Criando sala {sala_id} entre {nome1} e {nome2}.")
        sala = Sala(jogador1, jogador2, nome1, nome2, self, sala_id)
        self.salas_ativas[sala_id] = {"sala": sala, "inicio": agora}
        sala.iniciar()
        self.medidas['salas_criadas'] += 1

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
            self.fila_espera.append((conn, nome, time.time()))
            self.medidas['inicio_fila'][nome] = time.time()
            if len(self.fila_espera) >= 2:
                self.iniciar_nova_sala()

    def exibir_metricas(self):
        total = len(self.medidas['tempo_em_fila'])
        media_fila = sum(self.medidas['tempo_em_fila']) / total if total > 0 else 0
        total_p = len(self.medidas['tempo_partidas'])
        media_partida = sum(self.medidas['tempo_partidas']) / total_p if total_p > 0 else 0

        with open("metricas_servidor.txt", "w") as f:
            f.write("[METRICAS DE DESEMPENHO]\n")
            f.write(f"- Jogadores atendidos: {total}\n")
            f.write(f"- Salas criadas: {self.medidas['salas_criadas']}\n")
            f.write(f"- Tempo medio na fila: {media_fila:.2f}s\n")
            f.write(f"- Tempo medio de partida: {media_partida:.2f}s\n")
            f.write(f"- Threads ativas: {len(threading.enumerate())}\n")

    def monitorar_comando(self):
        while self.rodando:
            comando = input()
            if comando.strip().lower() in ("sair", "exit", "quit"):
                self.rodando = False
                print("[SERVIDOR] Encerrando servidor e salvando métricas...")
                self.exibir_metricas()
                break

    def iniciar(self, host='localhost', porta=12345):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((host, porta))
        servidor.listen()
        print(f"[SERVIDOR] Iniciado em {host}:{porta}")

        threading.Thread(target=self.monitorar_comando, daemon=True).start()

        while self.rodando:
            try:
                servidor.settimeout(1.0)
                conn, addr = servidor.accept()
                threading.Thread(target=self.lidar_com_cliente, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue

if __name__ == '__main__':
    Servidor().iniciar()