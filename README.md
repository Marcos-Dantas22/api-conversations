# realmate-challenge

## Introdução

O objetivo deste desafio é avaliar seus conhecimentos em **APIs** e **Webhooks**, além da sua capacidade de aprender rapidamente e implementar soluções eficientes, usando frameworks renomados como **Django** e **Django Rest Framework (DRF)**.

Você deverá desenvolver uma web API que sincroniza eventos de um sistema de atendimentos no WhatsApp, processando webhooks e registrando as alterações no banco de dados.

## 🎯 O Desafio

Desenvolver uma web API utilizando **Django Rest Framework** para receber webhooks de um sistema de atendimento. Esses webhooks contêm eventos relacionados a conversas e mensagens, e devem ser registrados no banco de dados corretamente.

## 📌 Requisitos

1.	Criar dois modelos principais:
	- `Conversation`
	- `Message` (relacionado a uma `Conversation`)
2.	A API deve:
	- Receber eventos via POST no endpoint `localhost/webhook/`
	- Criar instâncias dos modelos correspondentes
3.	Criar um endpoint GET em `localhost/conversations/{id}` para expor a conversa, incluindo:
	- Seu estado (`OPEN` ou `CLOSED`)
	- Suas mensagens
4.	Lidar com erros de maneira graceful (evitar retornos de erro 500).
5.	Restrições:
	- Uma `Conversation` deve ter um estado. Os estados possíveis são: `OPEN` e `CLOSED`
	- Uma `CLOSED` `Conversation` não pode receber novas mensagens
	- Uma `Message` deve ter dois tipos: `SENT` e `RECEIVED`
6.	O banco de dados utilizado deve ser SQLite.

## 📦 Formato dos Webhooks

Os eventos virão no seguinte formato:

### Novo evento de conversa iniciada

```json
{
    "type": "NEW_CONVERSATION",
    "timestamp": "2025-02-21T10:20:41.349308",
    "data": {
        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Novo evento de mensagem recebida

```json
{
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:42.349308",
    "data": {
        "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
        "direction": "RECEIVED",
        "content": "Olá, tudo bem?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Novo evento de mensagem enviada

```json
{
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:44.349308",
    "data": {
        "id": "16b63b04-60de-4257-b1a1-20a5154abc6d",
        "direction": "SENT",
        "content": "Tudo ótimo e você?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Novo evento de conversa encerrada

```json
{
    "type": "CLOSE_CONVERSATION",
    "timestamp": "2025-02-21T10:20:45.349308",
    "data": {
        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

## 📌 Regras de Negócio

- Toda conversa começa no estado “OPEN”
- Uma conversa no estado “CLOSED” não pode receber novas mensagens
- As mensagens devem estar associadas a uma conversa existente
- O ID da mensagem e o ID da conversa devem ser únicos
- O sistema deve lidar com erros sem retornar HTTP 500

## 🔥 Bônus (Opcional)

Se quiser ir além e demonstrar sua capacidade de aprendizado e desenvolvimento rápido, você pode implementar um frontend simples para visualizar as conversas e mensagens.

## 🚀 Tecnologias e Ferramentas

- Django
- Django Rest Framework
- Poetry
- SQLite
- GitHub

## 📌 Instruções de Instalação

### Pré-requisitos

- Instalar o Poetry para gerenciamento de dependências:

```bash
pip install poetry
```

### Instalação do Projeto

> [!WARNING]  
> Siga todas as instruções de instalação do projeto. O descumprimento dos requisitos de instalação acarretará a desclassificação do(a) candidato(a).

1.	Crie um repositório público, utilizando este repositório como template. Para isso, clique sobre o botão "**Use this template**", no canto superio direito desta tela. Forks **não** serão aceitos.



2.	Instale as dependências do projeto utilizando o Poetry:

```bash
cd realmate-challenge
poetry install
```

3.	Aplique as migrações no banco de dados SQLite:

```bash
python manage.py migrate
```

4.	Execute o servidor de desenvolvimento:

```bash
python manage.py runserver
```


## 📌 Entrega e Requisitos

Após concluir o desafio, envie o link do repositório para o e-mail tecnologia@realmate.com.br com seu nome e número do WhatsApp informados no e-mail.

## 📚 Referências

- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django](https://www.djangoproject.com/)
- [Poetry](https://python-poetry.org/)

## 📧 Dúvidas

Caso tenha dúvidas sobre o desafio, entre em contato com nossa equipe de tecnologia no e-mail tecnologia@realmate.com.br.

Boa sorte! 🚀

_Equipe Realmate_

# 🚀 API Conversations

Uma poderosa e elegante API desenvolvida com **DjangoRestFramework**, seguindo as melhores práticas de segurança, testes, versionamento e deploy. Ideal para aplicações escaláveis e modernas.

---

## 🌐 Frontend da Aplicação

O frontend da aplicação pode ser acessado através do seguinte link:

🔗 **[Acessar Frontend](https://api-conversations.onrender.com/api/interface)**

## 🌐 Documentação

Acesse a documentação interativa da API no Swagger:

🔗 **[https://api-conversations.onrender.com/api/docs/](https://api-conversations.onrender.com/api/docs/)**

> ⚠️ *O projeto está hospedado na Render com plano gratuito (Free Tier), o que pode causar uma demora inicial de alguns segundos ao acessar após período de inatividade (cold start).*

---

## 🛠️ Tecnologias Utilizadas

- **[Python 3.13](https://www.python.org/)** – Linguagem de programação principal.
- **[SQLITE3](https://www.sqlite.org/)** – Banco de dados local para desenvolvimento.
- **[PostgreSQL](https://www.postgresql.org/)** – Banco de dados em produção.
- **[API Key](https://swagger.io/docs/specification/authentication/api-keys/)** – Autenticação segura via API key.
- **[Django](https://www.djangoproject.com/)** – Framework web utilizado para criar a API.
- **[Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)** – Utilizado para renderizar as páginas frontend, como a visualização de conversas e imóveis.
- **[djangorestframework](https://www.django-rest-framework.org/)** – Utilizado para facilitar a criação de APIs RESTful com Django.
- **[Sentry](https://sentry.io/)** – Monitoramento de erros em tempo real.
- **[GEMINI API](https://developers.google.com/search/blog/2022/05/introducing-gemini)** – API do Google para processamento de mensagens e busca de imóveis relacionados.
- **[Poetry](https://python-poetry.org/)** – Gerenciador de dependências e empacotamento para projetos Python.
---

## 📦 Como rodar o projeto com Docker

```bash
# Clone o projeto
git clone https://github.com/Marcos-Dantas22/api-conversations.git
cd api-conversations

# Gere o arquivo .env com as variáveis de ambiente
./setup.sh  # ou execute manualmente conforme abaixo

# Usuario admin disponivel em produção
username: useradmin
password: adminadmin
```

## Informações sobre o Desenvolvimento do Projeto
Este projeto consiste em uma API desenvolvida com Django + DjangoRestFramework + Poetry, utilizando SQLITE3 como banco de dados. A aplicação foi estruturada para atender aos requisitos de receber webhooks de um sistema de atendimento. Esses webhooks contêm eventos relacionados a conversas e mensagens, e devem ser registrados no banco de dados corretamente. Todos os endpoints foram cuidadosamente implementados, com validações adequadas e tratamento de erros para garantir a robustez da aplicação.

Além disso, foi implementada um frontend utilizando django templates, para visualizar as conversas e mensagens que são processadas.

![Tela de Conversas](api/static/images/Conversas-Page.png)

Existe também uma pagina de imoveis de exemplo

![Tela de Imóveis](api/static/images/Imoveis-Page.png)

Essa pagina serve como uma integração com uma funcionalidade de IA que eu adicionei utilizando o gemini do google, funciona da seguinte maneira: ao processar uma mensagem, se ela contem informações de busca de um imovel ela vai gerar uma instancia da classe LeadInfo, e ao entrar na pagina de imoveis, ele vai buscar pra cada imovel se existem instancias de LeadInfo relacionadas a algum imovel, utilizando o tipo de imovel, bairro e numero de quartos. Dessa forma vai aparecer sinalizada na pagina que aquele imovel tem alguem interessado e ao entrar nos detalhes do imovel vai mostrar o id da conversa que esta interessada.

A aplicação está hospedada na plataforma Render, o que pode ocasionar um pequeno tempo de espera na primeira requisição, já que o serviço entra em modo de inatividade depois de 15 min de inatividade para otimizar recursos. Porém, após a primeira requisição, a API transita para outro modo, garantindo que as requisições subsequentes sejam respondidas com o tempo normal de latência.