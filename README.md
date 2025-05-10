# Jogo da Velha Multijogador com Fila

## Funcionalidades corretas:
    - Nome de login para o jogador (apenas para controle visual)
    - Fila de espera
    - Conexão entre pares
    - Lógica do jogo da velha
    - Jogar novamente (se ambos quiserem)
    - Encerrar a PRÓPRIA conexão a qualquer momento (digitando SAIR)
    - Jogador volta para a fila quando encerra um jogo
        - Quando o outro desiste no meio ou quando não quer continuar jogando

## Erros:
    - O jogador retornar para a fila na opção quer quer continuar jogando mas o outro diz primeiro que vai sair (O encerra a conexão normalmente de um mas o outro não volta para a fila)

## Últimas correções:
    - Ao encerrar a partida se um deles quiser continuar ele volta para a fila
    - Encerrando a conexão da sala corretamente
    - Adicionado nome de login para controle visual


## Não implementado
    - Métricas de desempenho que servivam pra comparar paralelismo e sequencial ?

