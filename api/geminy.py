import google.generativeai as genai
import os
import json
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extrair_lead_info(content):
    prompt = f"""
        Se o texto for alguem em busca de um imovel.
        Extraia as seguintes informações da mensagem abaixo:
        - tipo_imovel (ex: casa, apartamento, kitnet)
        - bairro
        - faixa_preco (ex: até 600 mil, entre 2 e 3 mil por mês)
        - quartos (número inteiro)
        - urgencia (baixa, média ou alta)

        Mensagem: "{content}"

        Responda apenas em JSON com as chaves exatas:
        type_property, neighborhood, price_track, rooms, urgency
        Se o texto não conter alguns desses campos, retornar como None o valor
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    clean_text = re.sub(r"^```json\n|\n```$", "", response.text.strip(), flags=re.MULTILINE)

    try:
        parsed = json.loads(clean_text)
        # print("JSON parseado:", parsed)
        return parsed
    except json.JSONDecodeError as e:
        # print("Erro ao parsear JSON:", e)
        return {}
