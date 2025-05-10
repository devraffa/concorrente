## cliente.py
import socket
import threading

def receber_mensagens(sock):
    while True:
        try:
            mensagem = sock.recv(1024).decode()
            if not mensagem:
                break
            if mensagem.strip().startswith("┌") or "│" in mensagem:
                print(mensagem, end='')  # imprime o tabuleiro sem prefixo
            elif mensagem.strip().upper() == "DESCONECTADO":
                print("[CLIENTE] Você foi desconectado pelo servidor.")
                sock.close()
                return
            elif mensagem.strip() != "":
                print(f"[CLIENTE] {mensagem.strip()}")
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
    nome = input("Digite seu nome de login: ")
    sock.sendall(nome.encode())
    print("[CLIENTE] Conectado ao servidor! Aguardando outro jogador...")

    t = threading.Thread(target=receber_mensagens, args=(sock,), daemon=True)
    t.start()
    enviar_para_servidor(sock)
    t.join()

if __name__ == "__main__":
    main()