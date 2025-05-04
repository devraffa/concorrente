import socket
import threading

clientes = []
fila = []

def broadcast_mensagem(msg):
    for cliente in clientes:
        try:
            cliente.sendall(msg.encode())
        except:
            pass

def lidar_com_cliente(conexao, endereco):
    print(f"[+] Conectado com {endereco}")
    clientes.append(conexao)
    while True:
        try:
            dados = conexao.recv(1024).decode()
            if not dados:
                break
            if dados == "Okay":
                if endereco not in fila:
                    fila.append(endereco)
            elif dados == "Sair":
                if endereco in fila:
                    fila.remove(endereco)
            print(f"[Fila] {fila}")
            broadcast_mensagem(f"Pessoas na fila: {len(fila)}")
        except:
            break
    conexao.close()
    if conexao in clientes:
        clientes.remove(conexao)
    if endereco in fila:
        fila.remove(endereco)
    broadcast_mensagem(f"Pessoas na fila: {len(fila)}")
    print(f"[-] Desconectado {endereco}")

def iniciar_servidor(host='localhost', porta=12345):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen()
    print(f"[Servidor] Aguardando conexões em {host}:{porta}...")
    while True:
        conexao, endereco = servidor.accept()
        threading.Thread(target=lidar_com_cliente, args=(conexao, endereco)).start()

if __name__ == "__main__":
    
    iniciar_servidor()
