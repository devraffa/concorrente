# servidor.py
import socket
import threading
from sala import Sala

fila_espera = []
fila_lock = threading.Lock()

def lidar_com_cliente(conn, addr):
    print(f"[INFO] Novo jogador conectado: {addr}")
    try:
        conn.sendall(b"Conectado ao servidor!\nAguardando outro jogador...\n")
    except:
        print(f"[ERRO] Falha ao enviar mensagem para {addr}")
        conn.close()
        return
    

    while True:
        with fila_lock:
            fila_espera.append(conn)
            if len(fila_espera) >= 2:
                jogador1 = fila_espera.pop(0)
                jogador2 = fila_espera.pop(0)
                print(f"[INFO] Emparelhando {jogador1.getpeername()} e {jogador2.getpeername()}")
                sala = Sala(jogador1, jogador2)
                sala.iniciar()
        break

def iniciar_servidor(host='localhost', porta=12345):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen()
    print(f"[SERVIDOR] Iniciado em {host}:{porta}")

    while True:
        conn, addr = servidor.accept()
        threading.Thread(target=lidar_com_cliente, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    iniciar_servidor()
