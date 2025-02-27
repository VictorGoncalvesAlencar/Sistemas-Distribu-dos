import socket
import json
import datetime

SERVER_IP = 'victor-sd.ddns.net'
SERVER_PORT = 55555

def configure_server():
    global SERVER_IP, SERVER_PORT
    print("\nConfigurar Servidor")
    new_ip = input(f"Digite o novo IP do servidor (atual: {SERVER_IP}): ").strip() or SERVER_IP
    new_port = input(f"Digite a nova porta do servidor (atual: {SERVER_PORT}): ").strip() or SERVER_PORT
    try:
        new_port = int(new_port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(2)
            client.connect((new_ip, new_port))
            SERVER_IP, SERVER_PORT = new_ip, new_port
            print("Serviço Disponível! Configuração salva.")
    except (socket.error, ValueError):
        print("Falha ao conectar. Mantendo configurações atuais.")

def send_request(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, SERVER_PORT))
        client.send(json.dumps(data).encode())
        response = json.loads(client.recv(1024).decode())
    return response

def register():
    name = input("Nome completo: ")
    username = input("Username (sem espaços): ").strip().replace(" ", "")
    if not username:
        print("Username inválido.")
        return
    password = input("Senha: ")  # Envia a senha em texto plano
    response = send_request({
        "action": "register",
        "name": name,
        "username": username,
        "password": password
    })
    print(response["message"])

def login():
    global logged_in_user
    username = input("Username: ").strip()
    password = input("Senha: ")  # Envia a senha em texto plano
    response = send_request({
        "action": "login",
        "username": username,
        "password": password
    })
    if response["status"] == "success":
        logged_in_user = username
        print(f"\nBem-vindo, {response['name']}!")
        main_menu()
    else:
        print(response["message"])

def send_email():
    if not logged_in_user:
        print("Você precisa estar logado para enviar e-mails.")
        return

    recipient = input("Destinatário: ")
    subject = input("Assunto: ")
    body = input("Mensagem: ")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    response = send_request({
        "action": "send_email",
        "from": logged_in_user,
        "to": recipient,
        "timestamp": timestamp,
        "subject": subject,
        "body": body
    })
    
    print(response["message"])

def receive_emails():
    if not logged_in_user:
        print("Você precisa estar logado para receber e-mails.")
        return
    response = send_request({
        "action": "receive_emails",
        "username": logged_in_user
    })
    if response["emails"]:
        print(f"\n{len(response['emails'])} e-mails recebidos:")
        for i, email in enumerate(response["emails"], 1):
            print(f"[{i}] {email['from']}: {email['subject']}")
        choice = int(input("\nQual e-mail deseja ler? ")) - 1
        if 0 <= choice < len(response["emails"]):
            email = response["emails"][choice]
            print(f"\nDe: {email['from']}\nAssunto: {email['subject']}\nMensagem: {email['body']}")
    else:
        print("Nenhum e-mail novo.")

def main_menu():
    while True:
        print("\n1) Enviar E-mail\n2) Receber E-mails\n3) Logout")
        option = input("Escolha uma opção: ")
        if option == "1":
            send_email()
        elif option == "2":
            receive_emails()
        elif option == "3":
            print("Logout realizado.")
            break
        else:
            print("Opção inválida.")

def start_client():
    global logged_in_user
    logged_in_user = None
    while True:
        print("\n1) Apontar Servidor\n2) Cadastrar Conta \n3) Acessar E-mail \n4) Sair ")
        option = input("Escolha uma opção: ")
        if option == "1":
            configure_server()
        elif option == "2":
            register() 
        elif option == "3":
            login() 
        elif option == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    start_client()

