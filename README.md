Este projeto foi desenvolvido utilizando Python e Flask com o objetivo de praticar conceitos importantes de desenvolvimento backend, como:

*CRUD de usuários

*Autenticação com JWT

*Autorização por níveis de acesso (roles)

*Relacionamentos com SQLAlchemy

*Migrations com Flask-Migrate

*Testes automatizados com Pytest

*Estruturação de API REST


O sistema possui autenticação baseada em token e controle de permissões, permitindo diferenciar usuários administradores de usuários comuns.

# Autenticação JWT

## Login

POST /auth/login

### Body

{

  "username": "admin",

  "password": "123"

}

### Resposta

{

  "access_token": "TOKEN"

}

## Usando o Token

Authorization: Bearer TOKEN