# Introdução ao Pytest

Este repositório **es-pytest** tem foco em:

- Escrever testes automatizados com **pytest**
- Estruturar um pequeno projeto em **FastAPI** voltado para testes
- Integrar os testes em um fluxo de **CI** simples
- Rodar os testes em diferentes contextos: local, Docker e Kubernetes

A aplicação FastAPI aqui é propositalmente simples: ela existe principalmente para servir de **alvo de testes**.

## Estrutura do Repositório

```text
es-pytest/
├── .github/workflows/       # GitHub Actions para CI
│   └── ci.yml               # CI: executa pytest e gera relatório de cobertura
├── app/                     # Aplicação FastAPI + testes
│   ├── main.py              # Aplicação FastAPI (alvo dos testes)
│   ├── test_main.py         # Testes escritos com pytest
│   └── requirements.txt     # Dependências Python
├── k8s/                     # Manifests Kubernetes (Kustomize)
│   ├── deployment.yaml      # Deployment da aplicação
│   ├── service.yaml         # Service para exposição
│   └── kustomization.yaml   # Configuração do Kustomize
├── Dockerfile               # Imagem da aplicação FastAPI
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

## Como Rodar Localmente (foco em testes)

### 1. Clonar o Repositório

```bash
git clone https://github.com/gabriel04alves/es-pytest.git
cd es-pytest
```

### 2. Criar e Ativar o Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
# venv\Scripts\activate     # Windows (PowerShell/CMD)
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
pytest -v
```

Para rodar com **relatório de cobertura**:

```bash
pytest --cov=main --cov-report=term-missing
```

Você também pode rodar um teste específico, por exemplo:

```bash
pytest -k square
```

### 5. Iniciar a Aplicação (para inspecionar manualmente)

Depois de garantir que os testes passam, você pode subir a API para explorar os endpoints.

```bash
cd app
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Acesse [http://localhost:8000](http://localhost:8000)

#### Endpoints disponíveis

> A aplicação é simples, mas os endpoints foram desenhados para permitir escrever testes
> que cobrem casos de sucesso **e** de erro/validação.

| Método | Rota          | Descrição rápida                                                                                                                                                                                                            |
| ------ | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- | ------------------------------------------------- |
| `GET`  | `/`           | Health-check simples: retorna `{ "message": "Hello World!!!" }`.                                                                                                                                                            |
| `GET`  | `/square/{x}` | Retorna `{ "result": x * x }`. Se `                                                                                                                                                                                         | x   | > 10000`, retorna **400** com `"x is too large"`. |
| `GET`  | `/double`     | Usa query params. `?x=4` retorna `{ "result": 8 }`. Com `validated=true`, só aceita `-100 <= x <= 100`; fora disso retorna **422**.                                                                                         |
| `GET`  | `/stats`      | Recebe vários `numbers` por query (`/stats?numbers=1&numbers=2&numbers=3`) e retorna contagem, soma, média, min e max. Quando os parâmetros obrigatórios não são enviados, o FastAPI retorna **422** com erro de validação. |

Os testes em `app/test_main.py` verificam, por exemplo:

- que os endpoints felizes (200) estão corretos (`/`, `/square/3`, `/double?x=4`, `/stats?numbers=1&numbers=2&numbers=3`);
- que o FastAPI levanta **400** ou **422** em cenários inválidos (por exemplo, `x` muito grande em `/square/{x}` ou ausência de parâmetros obrigatórios em `/stats`).

## Pytest no Contexto de DevOps

Além de rodar localmente, o mesmo comando `pytest` é usado em:

- **Pipelines de CI** (GitHub Actions)
- **Build de imagens Docker** (rodar testes antes de gerar a imagem)

## Containerização com Docker (com foco em testes)

1. **Build da imagem** da aplicação:

   ```bash
   docker build -t es-pytest:latest .
   ```

2. **Executar o container** localmente:

   ```bash
   docker run -p 8000:8000 es-pytest:latest
   ```

3. (Opcional) **Rodar pytest dentro do container**:

   ```bash
   docker run es-pytest:latest pytest
   ```

## CI com GitHub Actions

O projeto inclui um workflow de CI configurado em `.github/workflows/ci.yml`.

### Workflow de CI

Executa automaticamente a cada **push** ou **pull request** na branch `main`:

1. Configuração do Python 3.13
2. Instalação das dependências
3. Execução dos testes (`pytest -v`)
4. Geração do relatório de cobertura de código
5. Upload do relatório como artefato

O ponto principal é observar como o **pytest** entra nesses fluxos automáticos para garantir qualidade contínua.

---

## Recursos Adicionais

- [Documentação do Pytest](https://docs.pytest.org/)
- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [pytest-cov - Plugin de Cobertura](https://pytest-cov.readthedocs.io/)
- [GitHub Actions](https://docs.github.com/pt/actions)
