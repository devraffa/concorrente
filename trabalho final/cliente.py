import socket
import threading

def ouvir_servidor(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(f"[Atualização] {msg}")
        except:
            print("[!] Conexão com servidor perdida.")
            break

def iniciar_cliente(host='localhost', porta=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, porta))
    threading.Thread(target=ouvir_servidor, args=(sock,), daemon=True).start()

    print("Digite 'Okay' para entrar na fila ou 'Sair' para sair.")
    while True:
        comando = input(">>> ").strip()
        if comando.lower() in ["okay", "sair"]:
            sock.sendall(comando.encode())
        else:
            print("Comando inválido.")

if __name__ == "__main__":
    
    iniciar_cliente()
