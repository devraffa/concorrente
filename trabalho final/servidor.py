import socket
import threading
from sala import Sala  # Certifique-se de que este arquivo está correto

fila_espera = []
fila_lock = threading.Lock()  # Protege o acesso à fila de espera

def lidar_com_cliente(conn, addr):
    print(f"Novo jogador conectado: {addr}")
    
    try:
        conn.sendall(b"Conectado ao servidor!\nAguardando outro jogador...\n")
    except:
        print(f"Erro ao enviar mensagem para {addr}")
        conn.close()
        return

    with fila_lock:
        fila_espera.append(conn)
        if len(fila_espera) >= 2:
            jogador1 = fila_espera.pop(0)
            jogador2 = fila_espera.pop(0)
            print(f"Emparelhando jogadores {jogador1.getpeername()} e {jogador2.getpeername()}")
            threading.Thread(target=Sala, args=(jogador1, jogador2)).start()

def iniciar_servidor(host='localhost', porta=12345):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen()
    print(f"Servidor iniciado em {host}:{porta}")

    while True:
        conn, addr = servidor.accept()
        threading.Thread(target=lidar_com_cliente, args=(conn, addr)).start()

if __name__ == '__main__':
    iniciar_servidor()
