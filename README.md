# HS-API

API do site da HackerSchool, feita com [FastAPI](https://fastapi.tiangolo.com/) e SQLite. Serve os dados dos **membros** e dos **projetos**, as **participações** (a ligação entre membros e projetos) e as **fotografias** dos membros.

## Funcionalidades

- **Membros:** criar, listar e consultar membros (nome, email, número IST, curso, cargos, descrição e GitHub).
- **Projetos:** criar, listar e consultar projetos (nome, slug, estado e descrição).
- **Participações:** associar membros a projetos e ver que projetos tem cada membro (e que membros tem cada projeto).
- **Imagens:** upload e consulta da fotografia de cada membro. Se o membro não tiver fotografia, a API devolve uma imagem por defeito.

A base de dados é um ficheiro SQLite (`hackerschool.db`) criado automaticamente no primeiro arranque, por isso não é preciso instalar nem configurar nenhum servidor de base de dados.

## Requisitos

- [uv](https://docs.astral.sh/uv/) (recomendado), **ou** Python 3.11+ com `pip`
- Git

## Instalação

```bash
git clone <https://github.com/HackerSchool/HS-API-Simple.git>
cd HS-API-Simple
```

### Com uv (recomendado)

```bash
uv sync
```

### Com pip

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Executar a API

Com uv:

```bash
uv run uvicorn src.main:app --reload
```

Com pip (com o ambiente virtual ativo):

```bash
uvicorn src.main:app --reload
```

A API fica disponível em `http://localhost:8000`.

## Documentação e testes

O FastAPI gera automaticamente uma documentação interativa em:

**http://localhost:8000/docs**

É aqui que podes ver todos os endpoints, criar membros e projetos de teste, fazer upload de fotografias e testar os pedidos diretamente no browser.

## Principais endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/members` | Criar um membro |
| `GET` | `/members` | Listar membros |
| `GET` | `/members/{ist_id}` | Consultar um membro |
| `GET` | `/members/{ist_id}/projects` | Projetos de um membro |
| `POST` | `/members/{ist_id}/projects/{slug}` | Associar um membro a um projeto |
| `POST` | `/members/{ist_id}/image` | Upload da fotografia (jpg/png) |
| `GET` | `/members/{ist_id}/image` | Obter a fotografia (ou a imagem por defeito) |
| `POST` | `/projects` | Criar um projeto |
| `GET` | `/projects` | Listar projetos |
| `GET` | `/projects/{slug}` | Consultar um projeto |
| `GET` | `/projects/{slug}/members` | Membros de um projeto |

## Estrutura do projeto

```
src/
  main.py            # arranque da aplicação e CORS
  database.py        # ligação à base de dados
  models/            # member.py, project.py, participation.py
  routers/           # members.py, projects.py
uploads/
  members/           # fotografias dos membros (<ist_id>.jpg / .png)
  defaults/          # imagem por defeito (default_member.png)
```

## Notas

- A imagem `uploads/defaults/default_member.png` tem de existir, caso contrário os membros sem fotografia dão erro.
