# Problema dos Filósofos

Este projeto é uma implementação do clássico "Problema dos Filósofos", um problema de sincronização em programação concorrente que envolve a coordenação de recursos compartilhados (neste caso, garfos) entre várias threads (os filósofos). Cada filósofo alterna entre pensar e comer, mas precisa pegar dois garfos para comer, o que traz desafios de sincronização para evitar deadlock e starvation.

## Descrição do Problema

No problema dos filósofos, temos cinco filósofos sentados em uma mesa redonda, cada um com um garfo à sua esquerda e à sua direita. Para comer, um filósofo precisa de ambos os garfos. O problema ocorre quando todos os filósofos tentam pegar os garfos ao mesmo tempo, levando a situações de deadlock ou starvation.

## Como o Código Funciona

- **Número de Filósofos**: 5
- **Tempo Limite de Espera** (`TEMPO_LIMITE_ESPERA`): 5 segundos - é o tempo máximo que um filósofo pode esperar antes de receber ajuda para comer.
- **Garfos**: São representados por semáforos (`threading.Lock()`), e cada filósofo precisa pegar dois garfos (um à sua esquerda e um à sua direita) para comer.

Cada filósofo é representado por uma thread que executa continuamente um ciclo de pensar e comer. A lógica é a seguinte:

1. **Pensar**: O filósofo passa algum tempo pensando.
2. **Esperar pelos Garfos**: Ele tenta pegar os garfos à sua esquerda e direita. Dependendo do seu ID, ele escolhe a ordem de pegar os garfos:
   - Filósofos de ID par pegam o garfo esquerdo primeiro.
   - Filósofos de ID ímpar pegam o garfo direito primeiro.
3. **Comer**: Assim que obtiver os dois garfos, o filósofo come por um tempo aleatório.
4. **Ceder os Garfos**: Depois de comer, o filósofo libera os garfos e volta a pensar.

## Resolução dos Problemas de Deadlock e Starvation

### Deadlock

O **deadlock** acontece quando cada filósofo segura um garfo e fica esperando pelo segundo garfo indefinidamente, impedindo que qualquer um deles consiga comer.

Nesta implementação, o deadlock é evitado pela estratégia de pegar os garfos de forma diferente para filósofos pares e ímpares:

- Filósofos **pares** pegam o garfo esquerdo primeiro, enquanto filósofos **ímpares** pegam o garfo direito primeiro.
- Essa abordagem de **ordem alternada** quebra a simetria que poderia causar um impasse, garantindo que não todos fiquem bloqueados ao tentar pegar um garfo que outro filósofo já possui.

### Starvation

**Starvation** ocorre quando um filósofo nunca consegue pegar os garfos necessários, enquanto outros filósofos conseguem comer repetidamente. 

Para evitar starvation, o código utiliza um **tempo limite de espera** (`TEMPO_LIMITE_ESPERA`). Se um filósofo não conseguir comer após esperar esse tempo limite:

1. Ele recebe ajuda dos **vizinhos**, forçando-os a ceder seus garfos temporariamente.
2. Isso é implementado pela função `com_ajuda_vizinhos()`, que permite que o filósofo faminto pegue os garfos e coma, garantindo que nenhum filósofo passe tempo demais sem se alimentar.

