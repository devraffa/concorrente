
# 🕹️ Jogo da Velha Multiplayer com Python e Sockets

Este projeto implementa um sistema cliente-servidor para partidas multiplayer de Jogo da Velha usando Python com sockets e multithreading. O servidor gerencia uma fila de espera, cria salas dinâmicas com dois jogadores e mantém métricas de desempenho.

## 🧱 Estrutura do Projeto

```
.
├── cliente.py           # Cliente interativo que se conecta ao servidor
├── servidor.py          # Servidor principal que lida com conexões e salas
├── sala.py              # Classe Sala que executa partidas entre dois jogadores
├── jogo.py              # Lógica do jogo da velha
├── metricas_servidor.txt (gerado dinamicamente)
```

## 🚀 Como Executar

### 1. Inicie o servidor

```bash
python servidor.py
```

Ele exibirá o IP local da máquina para que clientes possam se conectar, por exemplo:

```
[SERVIDOR] Iniciado em 0.0.0.0:12345
[INFO] IP local do servidor (conecte-se com esse IP): 192.168.0.10
```

### 2. Conecte dois clientes

Em outro terminal (ou outro computador na mesma rede):

```bash
python cliente.py
```

Digite o IP exibido pelo servidor e informe seu nome.

## 🎮 Como Funciona

### Cliente (`cliente.py`)
- Solicita IP e nome de login.
- Escuta mensagens do servidor em uma thread separada.
- Envia comandos digitados (número da jogada ou “SAIR”).

### Servidor (`servidor.py`)
- Aceita conexões e coloca os jogadores em uma fila.
- Quando há dois jogadores disponíveis, inicia uma nova sala.
- Mede e registra:
  - Tempo em fila por jogador.
  - Duração das partidas.
  - Número de salas criadas.
- Pode ser encerrado a qualquer momento com o comando `sair` (digitado no terminal).

### Sala (`sala.py`)
- Gerencia uma partida entre dois jogadores.
- Envia tabuleiro e solicita jogadas alternadamente.
- Detecta vitória, derrota ou empate.
- Após o fim da partida, pergunta a ambos se desejam jogar novamente:
  - Se ambos responderem “SIM”, a sala reinicia.
  - Se apenas um responder “SIM”, ele volta à fila de espera.
  - Se ambos disserem “SAIR” ou desconectarem, a sala é encerrada.

### Jogo (`jogo.py`)
- Implementa a lógica do Jogo da Velha tradicional.
- Controla o estado do tabuleiro e verifica vitória ou empate.

## 📊 Métricas de Desempenho

Ao encerrar o servidor com o comando sair, ele gera o arquivo metricas_servidor.txt com:

- Jogadores atendidos
- Salas criadas
- Tempo médio em fila
- Tempo médio de partidas
- Número de threads ativas

## 🛡️ Encerramento Seguro

- O cliente pode digitar `SAIR` a qualquer momento para encerrar a conexão.
- O servidor detecta desconexões e realoca o jogador restante.
- A thread da sala é encerrada assim que ambos os jogadores saem ou a partida termina.

## 💡 Melhorias Futuras

- Interface gráfica com tkinter ou pygame
- Persistência de histórico de partidas
- Modo espectador
- Chat entre jogadores
- Matchmaking por nível de habilidade

## 👩‍💻 Desenvolvido com

- Python 3.8+
- socket
- threading
- Orientação a objetos
