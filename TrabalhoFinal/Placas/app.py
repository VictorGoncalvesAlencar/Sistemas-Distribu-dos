import os
import json
import pika
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Configurações
UPLOAD_FOLDER = "Upload"
RABBITMQ_HOST = "localhost"  # Se o RabbitMQ estiver na mesma instância, ok
QUEUE_NAME = "image_queue"

# Cria a pasta de upload, se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Armazenamento dos resultados (em memória, para este exemplo)
results = {}  # Estrutura: { filename: resultado_processado }

# Configurar Flask
app = Flask(__name__)
CORS(app, origins=["http:sdplacaocr.duckdns.org"])  # Permitir CORS para todas as origens


# Configurar conexão com RabbitMQ para publicar tarefas
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

# ----------------------
# Rota para servir a interface web (index.html)
@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

# ----------------------
# Rota para receber o upload da imagem
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Obter o IP do cliente (pode ser usado para direcionar o resultado, se necessário)
    client_ip = request.remote_addr
    # Se for necessário um client_port, poderíamos recebê-lo via um campo extra no formulário.
    client_port = request.form.get("client_port", "N/A")  # Exemplo

    # Criar uma mensagem com os dados da tarefa em JSON
    task_message = json.dumps({
        "filename": filename,
        "client_ip": client_ip,
        "client_port": client_port  # se necessário
    })

    # Publica a tarefa na fila RabbitMQ
    channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=task_message)

    return jsonify({"message": "Arquivo enviado com sucesso", "filename": filename}), 200

# ----------------------
# Rota callback para receber o resultado do processamento do worker
@app.route("/result_callback", methods=["POST"])
def result_callback():
    data = request.get_json()
    if not data or "filename" not in data or "result" not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    filename = data["filename"]
    result = data["result"]

    # Armazena o resultado para ser consultado pelo cliente
    results[filename] = result

    return jsonify({"message": "Resultado recebido"}), 200

# ----------------------
# Rota para que o cliente obtenha o resultado do processamento
@app.route("/get_result", methods=["GET"])
def get_result():
    # O cliente deve enviar o nome do arquivo como query parameter: ?filename=...
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"error": "Parâmetro 'filename' é obrigatório"}), 400

    if filename in results:
        return jsonify({"result": results[filename]}), 200
    else:
        return jsonify({"message": "Processamento em andamento ou não encontrado."}), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
