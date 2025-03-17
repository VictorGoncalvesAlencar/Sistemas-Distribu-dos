Ótimo! Vou te passar um **passo a passo completo** para configurar o ambiente local e rodar a aplicação. Assim, você pode clonar o repositório do Git e executar sem problemas.

---

### 🔧 **Passo a Passo para Configurar o Ambiente Local**

#### **1️⃣ Clonar o Repositório**
Se ainda não clonou, faça isso com o comando:
```sh
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

---

#### **2️⃣ Criar e Ativar um Ambiente Virtual**
No Windows (PowerShell):
```sh
python -m venv venv
venv\Scripts\activate
```
No Linux/macOS:
```sh
python3 -m venv venv
source venv/bin/activate
```

---

#### **3️⃣ Atualizar o Pip**
```sh
python -m pip install --upgrade pip
```

---

#### **4️⃣ Instalar Dependências**
Dentro do ambiente virtual, execute:
```sh
pip install -r requirements.txt
```
Se não tiver um `requirements.txt`, crie um com as seguintes dependências:
```
flask
flask-cors
pika
requests
psutil
```
E então instale:
```sh
pip install -r requirements.txt
```

---

#### **5️⃣ Configurar o RabbitMQ**
Se estiver rodando localmente, você precisa do RabbitMQ. Se ainda não instalou, siga estes passos:

**No Windows (via Chocolatey):**
```sh
choco install rabbitmq
rabbitmq-server start
```

**No Linux (Ubuntu/Debian):**
```sh
sudo apt update
sudo apt install rabbitmq-server -y
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
```

Se estiver usando o RabbitMQ em uma máquina separada (exemplo: AWS), certifique-se de configurar o IP correto no código.

---

#### **6️⃣ Rodar o Servidor**
Dentro da pasta do projeto, execute:
```sh
python app.py
```

---

#### **7️⃣ Rodar o Worker**
Em outro terminal (com o ambiente virtual ativado), execute:
```sh
python worker.py
```

---

#### **8️⃣ Testar a Aplicação**
- **Frontend:** Abra o `index.html` no navegador.
- **Backend:** O servidor deve estar rodando no `http://localhost:5000`.
- **Envio de Imagem:** Teste o envio de uma imagem pelo frontend ou via Postman:
```sh
curl -X POST -F "file=@imagem.jpg" http://localhost:5000/upload
```

---

Se der algum erro, me avise que a gente resolve! 🚀
