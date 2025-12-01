## Seminário: Introdução ao Pytest com FastAPI

Este repositório **es-pytest** será usado em um seminário de introdução ao Pytest, com foco em:

- Escrever testes automatizados com **pytest**
- Estruturar um pequeno projeto em **FastAPI** voltado para testes
- Integrar os testes em um fluxo de **CI/CD** simples
- Rodar os testes em diferentes contextos: local, Docker e Kubernetes

A aplicação FastAPI aqui é propositalmente simples: ela existe principalmente para servir de **alvo de testes**.

## Estrutura do Repositório

```text
es-pytest/
├── .github/workflows/        # GitHub Actions (opcional para CI/CD)
│   ├── ci.yml               # CI: roda pytest, build e push da imagem Docker
│   └── cd.yml               # CD: atualização de kustomize (exemplo)
├── app/                     # Aplicação FastAPI + testes
│   ├── main.py              # Aplicação FastAPI (alvo dos testes)
│   ├── test_main.py         # Testes escritos com pytest
│   └── requirements.txt     # Dependências Python
├── k8s/                     # Manifests Kubernetes (Kustomize)
│   ├── deployment.yaml      # Deployment da aplicação
│   ├── service.yaml         # Service para exposição
│   └── kustomization.yaml   # Configuração do Kustomize
├── Dockerfile               # Imagem da aplicação FastAPI para testes
├── kind.yaml                # Cluster Kind local para demonstração
└── README.md                # Este arquivo
```

## Pré-requisitos

- **Git** (>=2.25)
- **Python** (>=3.8)
- **pip**
- **virtualenv** ou venv nativo
- **Docker** (para rodar em container)
- **kubectl**, **Kind** e **Kustomize** (para a parte de Kubernetes)

## Foco do Seminário: Pytest

Durante o seminário vamos responder principalmente:

- Como estruturar testes em um projeto Python?
- Como o pytest descobre testes automaticamente?
- Como escrever **testes de unidade** simples para funções/rotas do FastAPI?
- Como rodar os testes localmente, em CI e em um container Docker?

O arquivo principal de testes é `app/test_main.py`, contendo **pelo menos três testes** cobrindo os endpoints da aplicação.

## Como Rodar Localmente (foco em testes)

### 1. Clonar o Repositório

```bash
git clone https://github.com/SEU_USUARIO/es-pytest.git
cd es-pytest
```

### 2. Criar e Ativar o Ambiente Virtual

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.# .venv\\Scripts\\activate   # Windows (PowerShell/CMD)
```

### 3. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r app/requirements.txt
```

### 4. Rodar Testes com Pytest

Neste projeto, vamos sempre priorizar **rodar os testes antes de subir a aplicação**.

```bash
cd app
pytest
```

Você também pode rodar um teste específico, por exemplo:

```bash
cd app
pytest -k square
```

### 5. Iniciar a Aplicação (para inspecionar manualmente)

Depois de garantir que os testes passam, você pode subir a API para explorar os endpoints.

```bash
cd app
python main.py
```

Ou usando uvicorn:

```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Acesse [http://localhost:8000](http://localhost:8000)

#### Endpoints disponíveis

- `GET /` → `{ "message": "Hello World!!!" }`
- `GET /square/{x}` → `{ "result": x * x }`
- `GET /double/{x}` → `{ "result": x * 2 }`

Os testes em `test_main.py` verificam justamente se esses endpoints estão se comportando como esperado.

## Pytest no Contexto de DevOps

Além de rodar localmente, o mesmo comando `pytest` é usado em:

- **Pipelines de CI** (GitHub Actions)
- **Build de imagens Docker** (rodar testes antes de gerar a imagem)
- **Execução em ambientes de staging** (por exemplo, rodar smoke tests após deploy)

## Containerização com Docker (com foco em testes)

1. Build da imagem da aplicação de exemplo `es-pytest`:

   ```bash
   docker build -t SEU_DOCKERHUB/es-pytest:latest .
   ```

2. Executar o container localmente:

   ```bash
   docker run -p 8000:8000 SEU_DOCKERHUB/es-pytest:latest
   ```

3. (Opcional) Rodar pytest **dentro** do container (dependendo de como o Dockerfile estiver configurado):

   ```bash
   docker run SEU_DOCKERHUB/es-pytest:latest pytest
   ```

4. Push para o DockerHub:

   ```bash
   docker push SEU_DOCKERHUB/es-pytest:latest
   ```

## Kubernetes com Kind e Kustomize

Aqui o objetivo é mostrar como uma aplicação simples (testada com pytest) pode ser empacotada e executada em um cluster local.

### 1. Criar cluster Kind

```bash
kind create cluster --name es-pytest --config kind.yaml
```

### 2. Deploy com Kustomize

```bash
kubectl apply -k k8s/
```

### 3. Testar via port-forward

```bash
kubectl port-forward svc/es-pytest-service 8000:8000
```

Acesse [http://localhost:8000](http://localhost:8000)

## CI/CD com GitHub Actions (Opcional no Seminário)

Se você configurar os workflows em `.github/workflows/`, o fluxo típico será:

### Workflow de CI (`.github/workflows/ci.yml`)

Executa a cada push:

1. Configuração do Python (ex.: 3.11 ou 3.13)
2. Instalação das dependências
3. Execução dos testes (`pytest`)
4. Build e push da imagem Docker `SEU_DOCKERHUB/es-pytest:TAG`

### Workflow de CD (`.github/workflows/cd.yml`)

Executa a cada push na branch `main`:

1. Atualização do `kustomization.yaml` com a nova tag de imagem
2. Commit automático da mudança
3. Push das alterações

## Configuração de Secrets (para CI/CD)

Para o funcionamento do CI/CD com DockerHub, configure os seguintes secrets no GitHub:

- `DOCKERHUB_USERNAME`: Seu usuário do DockerHub
- `DOCKERHUB_TOKEN`: Token de acesso do DockerHub

O ponto principal é observar como o **pytest** entra nesses fluxos automáticos para garantir qualidade contínua.
