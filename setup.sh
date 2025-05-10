#!/bin/bash

# Verifica se o arquivo .env já existe
if [ ! -f .env ]; then
  # Cria o arquivo .env e adiciona as variáveis de ambiente
  echo "Criando arquivo .env com as variáveis necessárias..."

  cat <<EOL > .env
# Variáveis de ambiente do projeto
DEBUG=True
SECRET_KEY=-8qu$nurchgq%nm=+e58yu_^1h*@&#8xhfkk10n(tvjcxa-i6p
API_KEY=jEihI0vZj23aKgnxKkA91Xr6FPLGmJ7J7RH-v9dx4Xk
GEMINI_API_KEY=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DATABASE_URL=
POSTGRES_PORT=
EOL

  echo ".env criado com sucesso."

  # Garante que o arquivo .env tenha permissões seguras
  chmod 600 .env
  echo "Permissões de segurança configuradas para o arquivo .env."
  
else
  echo "O arquivo .env já existe. Nenhuma alteração foi feita."
fi

# Evita que o arquivo .env seja versionado no Git
if ! grep -q ".env" .gitignore; then
  echo ".env" >> .gitignore
  echo "Adicionado .env ao .gitignore para evitar versionamento."
else
  echo ".env já está no .gitignore."
fi

echo "Configuração concluída com sucesso!"
