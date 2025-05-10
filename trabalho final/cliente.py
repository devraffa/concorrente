## cliente.py
import socket
import threading

def receber_mensagens(sock):
    while True:
        try:
            mensagem = sock.recv(1024).decode()
            if not mensagem:
                break
            if mensagem.strip().upper() == "SAIR":
                print("[CLIENTE] Servidor encerrou a conexão.")
                sock.close()
                return
            print(mensagem)
        except:
            break

def enviar_para_servidor(sock):
    while True:
        try:
            msg = input()
            sock.sendall(msg.encode())
            if msg.strip().upper() == "SAIR":
                print("[CLIENTE] Você encerrou a conexão.")
                sock.close()
                return
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 12345))
    print("[CLIENTE] Conectado ao servidor!")

    threading.Thread(target=receber_mensagens, args=(sock,), daemon=True).start()
    enviar_para_servidor(sock)

if __name__ == "__main__":
    main()