import threading
import time
import random

# Número de filósofos (e garfos)
NUM_FILOSOFOS = 5
TEMPO_LIMITE_ESPERA = 5  # Tempo limite que um filósofo pode esperar para comer

# Semáforos para representar os garfos
garfos = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

# Lista para contar quantas vezes cada filósofo comeu
contagem_refeicoes = [0] * NUM_FILOSOFOS

# Lista para monitorar o tempo de espera de cada filósofo
tempo_espera = [0] * NUM_FILOSOFOS

# Função que representa o comportamento de um filósofo
def filosofo(id):
    while True:
        # Filósofo pensa por um tempo aleatório
        print(f"Filósofo {id} está pensando.")
        time.sleep(random.uniform(1, 3))  # Simula o tempo pensando

        # Inicia o tempo de espera
        inicio_espera = time.time()

        while True:
            # Tentativa de pegar os garfos (para comer)
            garfo_esquerdo = id
            garfo_direito = (id + 1) % NUM_FILOSOFOS

            # Verifica o tempo de espera
            tempo_espera[id] = time.time() - inicio_espera

            if tempo_espera[id] > TEMPO_LIMITE_ESPERA:
                print(f"Filósofo {id} está faminto demais! Vizinhos vão ajudá-lo.")
                # Forçar vizinhos a ceder os garfos
                com_ajuda_vizinhos(id, garfo_esquerdo, garfo_direito)
                break

            # Pega os garfos de forma controlada
            if id % 2 == 0:
                # Filósofos pares pegam o garfo esquerdo primeiro
                with garfos[garfo_esquerdo]:
                    with garfos[garfo_direito]:
                        comer(id)
                        break
            else:
                # Filósofos ímpares pegam o garfo direito primeiro
                with garfos[garfo_direito]:
                    with garfos[garfo_esquerdo]:
                        comer(id)
                        break

        # Depois de comer, o filósofo volta a pensar
        tempo_espera[id] = 0  # Reseta o tempo de espera após comer

# Função auxiliar para o filósofo comer
def comer(id):
    print(f"Filósofo {id} está comendo.")
    time.sleep(random.uniform(1, 2))  # Simula o tempo comendo
    contagem_refeicoes[id] += 1
    print(f"Filósofo {id} terminou de comer {contagem_refeicoes[id]} vez(es).")

# Função para os vizinhos ajudarem o filósofo faminto
def com_ajuda_vizinhos(id, garfo_esquerdo, garfo_direito):
    vizinho_esquerdo = (id - 1) % NUM_FILOSOFOS
    vizinho_direito = (id + 1) % NUM_FILOSOFOS

    # Vizinhos cedem temporariamente os garfos
    print(f"Filósofo {vizinho_esquerdo} e {vizinho_direito} estão ajudando o filósofo {id}.")
    with garfos[garfo_esquerdo], garfos[garfo_direito]:
        comer(id)
    print(f"Filósofo {vizinho_esquerdo} e {vizinho_direito} voltam ao comportamento normal.")

# Cria e inicia threads para cada filósofo
filosofos = [threading.Thread(target=filosofo, args=(i,)) for i in range(NUM_FILOSOFOS)]

for f in filosofos:
    f.start()

# Espera as threads terminarem (nunca acontecerá, já que o jantar é infinito)
for f in filosofos:
    f.join()
