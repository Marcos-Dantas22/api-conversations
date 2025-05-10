# api/populate_properts.py

from .models import Property

def populate_properts():
    examples = [
        {"type_property": "Apartamento", "neighborhood": "Centro", "price_track": "500k-700k", "rooms": 2},
        {"type_property": "Casa", "neighborhood": "Jardins", "price_track": "700k-900k", "rooms": 3},
        {"type_property": "Studio", "neighborhood": "Centro", "price_track": "300k-500k", "rooms": 1},
        {"type_property": "Casa", "neighborhood": "Zona Norte", "price_track": "400k-600k", "rooms": 2},
    ]

    for data in examples:
        Property.objects.get_or_create(**data)

    print("Imóveis populados com sucesso!")
