import pika
import subprocess
import time
import psutil

# Configurações
RABBITMQ_HOST = 'localhost'  # Ou IP do servidor
QUEUE_NAME = 'image_queue'
MAX_WORKERS = 5  # Número máximo de workers simultâneos
TASK_THRESHOLD = 50  # Número de tarefas para disparar um novo worker

# Lista para armazenar os processos dos workers
workers = []

def get_queue_size():
    """ Retorna o número de mensagens na fila do RabbitMQ. """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        queue = channel.queue_declare(queue=QUEUE_NAME, passive=True)
        queue_size = queue.method.message_count
        connection.close()
        return queue_size
    except Exception as e:
        print("Erro ao acessar RabbitMQ:", e)
        return 0

def start_worker():
    """ Inicia um novo worker como processo separado. """
    if len(workers) < MAX_WORKERS:
        print("🔹 Iniciando um novo worker...")
        worker_process = subprocess.Popen(["python3", "worker.py"])
        workers.append(worker_process)

def stop_worker():
    """ Para um worker se a fila estiver vazia. """
    if workers:
        worker_to_kill = workers.pop()  # Remove o último worker da lista
        print("🔻 Finalizando um worker...")
        worker_to_kill.terminate()  # Encerra o processo do worker

def manage_workers():
    """ Verifica a fila e ajusta o número de workers. """
    while True:
        queue_size = get_queue_size()
        print(f"📌 Tamanho da fila: {queue_size}")

        if queue_size > TASK_THRESHOLD:
            start_worker()  # Inicia um novo worker se houver muitas imagens na fila
        elif queue_size == 0 and len(workers) > 1:
            stop_worker()  # Para workers extras se a fila estiver vazia

        time.sleep(20)  # Verifica a cada 5 segundos

if __name__ == "__main__":
    print("🚀 Gerenciador de Workers Iniciado...")
    manage_workers()
