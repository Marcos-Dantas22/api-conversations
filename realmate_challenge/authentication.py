from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class ApiKeyAuthenticationPersonal(BaseAuthentication):
    def authenticate(self, request):
        if settings.DEBUG == True:
            return None  
        
        # Pega o valor da chave do cabeçalho 'Authorization'
        api_key = request.headers.get('Authorization')
        
        # Valida se a chave está presente e se é a chave correta
        if api_key is None or api_key != f"ApiKey {settings.API_KEY}":
            raise AuthenticationFailed('Chave de API inválida ou ausente.')

        # Caso seja válida, retornamos a autenticação, mas sem informações adicionais (retorno de autenticação com None)
        return None

from drf_spectacular.extensions import OpenApiAuthenticationExtension

class ApiKeyAuthenticationPersonalExtension(OpenApiAuthenticationExtension):
    target_class = 'realmate_challenge.authentication.ApiKeyAuthenticationPersonal'
    name = 'ApiKeyAuthPersonal'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',  # O nome do cabeçalho
            'description': 'Autenticação via API Key Personalizada',
        }