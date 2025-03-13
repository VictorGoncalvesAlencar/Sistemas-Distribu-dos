import json
import pika
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# --- Função que simula o processamento da imagem ---
def process_image(filename):
    print(f"Processando a imagem: {filename}")
    time.sleep(2)  # Simula o tempo de processamento
    processed_result = f"{filename} processada com sucesso"
    print(f"Imagem processada: {filename}")
    return processed_result

# --- Função para enviar o resultado do processamento para o servidor Flask ---
def send_result_to_server(filename, result):
    callback_url = "http://localhost:5000/result_callback"  # Se o app estiver na mesma instância; ajuste conforme necessário
    payload = {
        "filename": filename,
        "result": result
    }
    try:
        r = requests.post(callback_url, json=payload)
        print("Resultado enviado ao servidor:", r.json())
    except Exception as e:
        print("Erro ao enviar resultado:", e)

# --- Função executada para cada tarefa (usada pelo executor) ---
def process_image_task(ch, method, properties, body):
    # A mensagem é um JSON com os dados da tarefa
    task = json.loads(body.decode('utf-8'))
    filename = task.get("filename")
    # Você pode também obter client_ip e client_port, se necessário:
    client_ip = task.get("client_ip")
    client_port = task.get("client_port")
    
    # Processa a imagem usando o executor
    future = executor.submit(process_image, filename)
    result = future.result()
    
    # Envia o resultado de volta ao servidor (que poderá repassar ao cliente)
    send_result_to_server(filename, result)
    
    # Confirma a mensagem para que ela seja removida da fila
    ch.basic_ack(delivery_tag=method.delivery_tag)

# --- Configuração do RabbitMQ e do executor ---
def setup_rabbitmq():
    # Conecta ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='image_queue')
    
    # Cria um pool de threads para processar tarefas de forma concorrente
    global executor
    executor = ThreadPoolExecutor(max_workers=5)  # Número de workers simultâneos
    
    # Consome mensagens da fila usando a função de callback
    channel.basic_consume(queue='image_queue', on_message_callback=process_image_task)
    
    print('Worker aguardando por mensagens. Pressione CTRL+C para sair.')
    channel.start_consuming()

if __name__ == "__main__":
    setup_rabbitmq()
