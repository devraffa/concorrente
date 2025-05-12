# Jogo da Velha Multijogador com Fila

## Funcionalidades corretas:
    - Nome de login para o jogador (apenas para controle visual)
    - Fila de espera
    - Conexão entre pares
    - Lógica do jogo da velha
    - Jogar novamente (se ambos quiserem)
    - Encerrar a PRÓPRIA conexão a qualquer momento (digitando SAIR)
    - Jogador volta para a fila quando encerra um jogo (TODOS OS CASOS)

## Erros:
    - Não está com a mensagem de "Não é sua vez" e isso faz com que ele guarde a resposta e quando chega a vez dele a entrada anterior é jogada (tanto uma jogada válida quanto inválida)

## Últimas correções:
    - O jogador retornar para a fila na opção quer quer continuar jogando mas o outro diz primeiro que vai sair (O encerra a conexão normalmente de um mas o outro não volta para a fila)

## Não implementado
    - Métricas de desempenho que servivam pra comparar paralelismo e sequencial ?

