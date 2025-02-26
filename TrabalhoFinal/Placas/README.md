# INSTITUTO FEDERAL DE EDUCAÇÃO CIÊNCIA E TECNOLOGIA
## DO NORTE DE MINAS GERAIS - CAMPUS JANUÁRIA
### BACHARELADO EM SISTEMAS DE INFORMAÇÃO

---

### Equipe: Stefany Lima, Tássia Pereira e Victor Gonçalves

## Sistema Distribuído para Reconhecimento de Placas Veiculares

---

**Januária 2025**  
**Projeto Final - Sistemas Distribuídos**

## Proposta Geral
O projeto consiste em um Sistema Distribuído para Reconhecimento de Placas Veiculares. A aplicação permite que imagens de placas de veículos sejam enviadas para processamento por um servidor, retornando o texto da placa extraído. O sistema é baseado em uma arquitetura cliente-servidor assíncrona, permitindo escalabilidade e paralelismo no processamento das imagens.

### Cenário de Uso
- Um cliente envia uma imagem de uma placa para um servidor via API REST.
- O servidor armazena a imagem em uma fila de mensagens.
- Vários trabalhadores processam as imagens de forma distribuída, utilizando OpenCV para detecção da placa e EasyOCR para reconhecimento do texto.
- O resultado é armazenado e posteriormente recuperado pelo cliente.

## Tecnologias Adotadas

### Linguagens e Bibliotecas
- **Python** (Backend e processamento das imagens)
- **Flask** (API REST para comunicação entre cliente e servidor)
- **OpenCV** (Detecção das placas veiculares)
- **EasyOCR** (Reconhecimento de caracteres)
- **concurrent.futures** (Processamento assíncrono das imagens)
- **Pika** (Integração com RabbitMQ)

### Frameworks e Protocolos
- **RabbitMQ** (Mensageria para processamento distribuído)
- **Flask** (Framework para exposição da API REST)
- **HTTP/REST** (Protocolo de comunicação entre cliente e servidor)
- **JSON/Pickle** (Serialização de dados)
- **AWS EC2** (Infraestrutura distribuída na nuvem)

## Justificativa
O projeto está diretamente relacionado aos principais conceitos abordados na disciplina de Sistemas Distribuídos, pois envolve:
- **Processamento Distribuído**: As imagens são processadas em paralelo por múltiplos workers.
- **Mensageria Assíncrona**: RabbitMQ gerencia a distribuição das tarefas.
- **Escalabilidade**: A arquitetura permite adição de mais workers para lidar com alto volume de requisições.
- **Comunicação entre Módulos**: O sistema cliente-servidor opera por meio de APIs REST e filas de mensagens.
- **Elasticidade**: Workers podem ser escalados dinamicamente na AWS conforme a demanda.

## Equipe e Responsabilidades

| Nome    | Responsabilidade  |
|---------|------------------|
| Victor  | Backend e API REST (Flask, RabbitMQ) |
| Stefany | Processamento de imagens (OpenCV, EasyOCR) |
| Victor  | Infraestrutura e DevOps (AWS, Configuração de Workers) |
| Tassia  | Cliente e Interface Web |

## Repositório do Trabalho Final


