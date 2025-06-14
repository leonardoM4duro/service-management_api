# Service Management System

Sistema de gerenciamento de serviços desenvolvido com FastAPI, MongoDB (Beanie ODM) e autenticação JWT. Permite o cadastro, consulta, atualização e remoção de clientes e usuários, com rotas protegidas por autenticação.

## Tecnologias Utilizadas
- Python 3.10+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Beanie ODM](https://roman-right.github.io/beanie/) (MongoDB)
- [Motor](https://motor.readthedocs.io/) (Async MongoDB driver)
- [Pydantic](https://docs.pydantic.dev/)
- [Passlib](https://passlib.readthedocs.io/) (hash de senhas)
- [python-jose](https://python-jose.readthedocs.io/) (JWT)

## Como rodar localmente
1. **Clone o repositório**
2. **Crie um ambiente virtual e ative:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate    # Windows
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure as variáveis de ambiente** (exemplo `.env`):
   ```env
   MONGODB_URI=mongodb://localhost:27017
   JWT_SECRET_KEY=sua_chave_secreta
   JWT_REFRESH_SECRET_KEY=sua_chave_refresh
   ```
5. **Execute a aplicação:**
   ```bash
   uvicorn app:app --reload
   ```

## Principais Rotas da API

### Autenticação
- `POST /auth/login` — Login, retorna access e refresh token
- `POST /auth/refresh-token` — Gera novo access token usando refresh token
- `POST /auth/test-token` — Testa se o token é válido

### Usuários
- `POST /users/user` — Cria usuário
- `GET /users/users` — Lista todos usuários
- `GET /users/user/{user_id}` — Busca usuário por ID
- `PUT /users/user` — Atualiza usuário
- `DELETE /users/user/{user_id}` — Remove usuário
- `GET /users/current_user` — Dados do usuário autenticado

### Clientes
- `GET /clients/clients` — Lista todos clientes
- `POST /clients/client` — Cria cliente
- `GET /clients/client/{client_id}` — Busca cliente por ID
- `PUT /clients/client/{client_id}` — Atualiza cliente
- `DELETE /clients/client/{client_id}` — Remove cliente

> **Todas as rotas (exceto login e refresh) exigem autenticação via Bearer Token.**

## Exemplo de Autenticação
1. **Login:**
   ```http
   POST /auth/login
   Content-Type: application/x-www-form-urlencoded
   {
     "username": "seu_usuario",
     "password": "sua_senha"
   }
   ```
   Resposta:
   ```json
   {
     "access_token": "...",
     "refresh_token": "...",
     "token_type": "bearer"
   }
   ```
2. **Usar o token nas requisições:**
   ```http
   Authorization: Bearer <access_token>
   ```

## Estrutura dos Modelos
### Usuário
- `name`, `username`, `email`, `hash_password`, `disabled`

### Cliente
- `name`, `email`, `phone`, `address`, `city`, `state`, `zip_code`, `disabled`

## Observações
- O projeto utiliza MongoDB como banco de dados.
- As respostas seguem o padrão:
  ```json
  {
    "success": true,
    "data": ...,
    "error": null
  }
  ```
- Para acessar as rotas protegidas, obtenha o token via login e envie no header `Authorization`.

---

Desenvolvido com FastAPI e Beanie ODM. 