#!/bin/bash

# Ativar o ambiente de trabalho do Poetry
cd realmate_challenge && poetry install

# Voltar uma pasta para executar os outros comandos
cd ..

# Realizar outras tarefas necessárias
python manage.py collectstatic --no-input
python manage.py migrate

# Criar superusuário automaticamente
# python manage.py shell << END
# from django.contrib.auth import get_user_model

# User = get_user_model()

# username = 'useradmin'
# password = 'adminadmin'
# email = 'admin@example.com'

# if not User.objects.filter(username=username).exists():
#     User.objects.create_superuser(username=username, password=password, email=email)
#     print(f'Superuser "{username}" criado com sucesso.')
# else:
#     print(f'Superuser "{username}" já existe.')
# END
