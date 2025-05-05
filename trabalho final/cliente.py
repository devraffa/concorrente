import socket

def conectar_ao_servidor():
    """
    Conecta o cliente ao servidor e gerencia o fluxo de comunicação.
    """
    try:
        # Cria o socket do cliente
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conecta ao servidor
        cliente_socket.connect(('localhost', 12345))  # Defina o IP e porta do servidor
        print("Conectado ao servidor!")
        
        # Recebe a mensagem inicial de boas-vindas e qual jogador é
        mensagem_inicial = cliente_socket.recv(1024).decode()
        print(mensagem_inicial)

        # Jogo da Velha - Loop de jogadas
        while True:
            # Exibe o tabuleiro
            tabuleiro = cliente_socket.recv(1024).decode()
            print(tabuleiro)

            # Recebe a mensagem de turno
            turno = cliente_socket.recv(1024).decode()
            print(turno)

            # Solicita a jogada do jogador
            jogada = input("Escolha sua jogada (1-9): ")

            # Envia a jogada para o servidor
            cliente_socket.sendall(jogada.encode())

            # Espera pela resposta do servidor sobre o andamento do jogo
            resultado = cliente_socket.recv(1024).decode()
            print(resultado)

            # Se o jogo acabou, pergunta se deseja continuar
            if "vencedor" in resultado or "empate" in resultado:
                resposta = input("Deseja continuar jogando com o mesmo parceiro? (sim/não): ")
                cliente_socket.sendall(resposta.encode())

                # Se o jogador não quiser continuar, encerra a conexão
                if resposta.lower() == "não":
                    print("Você optou por sair do jogo.")
                    break

        # Fecha a conexão com o servidor
        cliente_socket.close()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    conectar_ao_servidor()
