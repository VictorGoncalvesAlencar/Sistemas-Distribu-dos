import socket
import threading
import bcrypt
import json
import datetime
from concurrent.futures import ThreadPoolExecutor

# Armazena usuários e e-mails temporariamente
users = {}  # {username: {"name": "Nome Completo", "password": hashed_password}}
emails = {}  # {destinatario: [{"from": remetente, "to": destinatário, "timestamp": data/hora, "subject": "Assunto", "body": "Mensagem"}]}

def log_operation(operation, details=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {operation}: {details}")

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            request = json.loads(data)
            action = request.get("action")
            log_operation("Requisição recebida", f"Ação: {action}")

            if action == "register":
                response = register_user(request)
            elif action == "login":
                response = authenticate_user(request)
            elif action == "send_email":
                response = send_email(request)
            elif action == "receive_emails":
                response = receive_emails(request)
            else:
                response = {"status": "error", "message": "Ação inválida"}

            client_socket.send(json.dumps(response).encode())
    except Exception as e:
        log_operation("Erro", str(e))
    finally:
        client_socket.close()
        log_operation("Conexão encerrada", "Cliente desconectado")

def register_user(data):
    username = data["username"]
    name = data["name"]
    password = data["password"].encode() 

    if username in users:
        log_operation("Tentativa de cadastro", f"Username {username} já existe")
        return {"status": "error", "message": "Usuário já existe."}

    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    users[username] = {"name": name, "password": hashed_password}
    log_operation("Cadastro realizado", f"Novo usuário: {username} ({name})")
    return {"status": "success", "message": "Usuário registrado com sucesso."}

def authenticate_user(data):
    username = data["username"]
    password = data["password"].encode()

    user = users.get(username)
    if not user or not bcrypt.checkpw(password, user["password"]):
        log_operation("Tentativa de login", f"Falha para usuário: {username}")
        return {"status": "error", "message": "Credenciais inválidas."}
    
    log_operation("Login realizado", f"Usuário: {username}")
    return {"status": "success", "message": f"Bem-vindo {user['name']}!", "name": user["name"]}

def send_email(data):
    sender = data["from"]
    recipient = data["to"]
    subject = data["subject"]
    body = data["body"]
    timestamp = data["timestamp"]

    if recipient not in users:
        log_operation("Envio de e-mail falhou", f"Destinatário não encontrado: {recipient}")
        return {"status": "error", "message": "Destinatário não encontrado."}

    if recipient not in emails:
        emails[recipient] = []
    
    emails[recipient].append({
        "from": sender,
        "to": recipient,
        "timestamp": timestamp,
        "subject": subject,
        "body": body
    })
    
    log_operation("E-mail enviado", f"De: {sender} Para: {recipient} - Assunto: {subject}")
    return {"status": "success", "message": "E-mail enviado com sucesso."}

def receive_emails(data):
    username = data["username"]
    user_emails = emails.pop(username, [])
    log_operation("Recebimento de e-mails", f"{len(user_emails)} e-mail(s) recebidos para {username}")
    return {"status": "success", "emails": user_emails}

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 55555))
    server.listen(5)
    log_operation("Servidor iniciado", "Rodando na porta 55555")

    with ThreadPoolExecutor() as executor:
        while True:
            client_socket, addr = server.accept()
            log_operation("Nova conexão", f"Endereço: {addr}")
            executor.submit(handle_client, client_socket)

if __name__ == "__main__":
    start_server()

