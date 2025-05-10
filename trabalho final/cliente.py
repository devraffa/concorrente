# cliente.py
import socket
import threading

def receber_mensagens(sock):
    while True:
        try:
            mensagem = sock.recv(1024).decode()
            if not mensagem:
                break
            if mensagem.strip().upper() == "SAIR":
                print("[CLIENTE] Conexão encerrada.")
                sock.close()
                return
            print(mensagem)
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 12345))
    print("[CLIENTE] Conectado ao servidor!")

    threading.Thread(target=receber_mensagens, args=(sock,), daemon=True).start()

    while True:
        try:
            msg = input()
            if msg.strip().upper() == "SAIR":
                sock.sendall("SAIR".encode())
                sock.close()
                break
            sock.sendall(msg.encode())
        except:
            break

if __name__ == "__main__":
    main()