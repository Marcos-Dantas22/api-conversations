#!/usr/bin/env bash
set -o errexit

# Entra na pasta correta
cd realmate_challenge

# Instala com Poetry
poetry install

# Coleta arquivos estáticos
poetry run python manage.py collectstatic --no-input

# Aplica as migrações
poetry run python manage.py migrate

# Cria o superusuário automaticamente
poetry run python manage.py shell << END
from django.contrib.auth import get_user_model

User = get_user_model()
username = 'useradmin'
password = 'adminadmin'
email = 'admin@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f'Superuser "{username}" criado com sucesso.')
else:
    print(f'Superuser "{username}" já existe.')
END
