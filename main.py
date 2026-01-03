import os, re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

VOWELS = "aeoáéóiuíúü"

import re

def rhyme_suffix(word: str) -> str:
    """
    Extrae la terminación vocálica tónica para comprobar rima asonante.
    Ejemplo: 'escudo' -> 'uo', 'verdugo' -> 'uo'.
    """
    # Limpieza básica
    w = word.lower().strip(".,;:!?'\"-")
    if not w:
        return ""

    vowels = "aeiouáéíóú"
    
    # Encontrar índices de todas las vocales
    v_indices = [i for i, char in enumerate(w) if char in vowels]
    if not v_indices:
        return "" # No hay vocales (ej. siglas o nums)

    # 1. Detectar sílaba tónica
    tonic_index = -1
    
    # A) Buscar tilde explícita
    for i in v_indices:
        if w[i] in "áéíóú":
            tonic_index = i
            break
            
    # B) Si no hay tilde, aplicar reglas de acentuación
    if tonic_index == -1:
        last_char = w[-1]
        # Regla: Si termina en vocal, n o s -> es Llana (penúltima sílaba)
        if last_char in "aeiouns":
            if len(v_indices) >= 2:
                tonic_index = v_indices[-2]
            else:
                tonic_index = v_indices[-1] # Monosílabos
        # Regla: Si termina en otra consonante -> es Aguda (última sílaba)
        else:
            tonic_index = v_indices[-1]

    # 2. Extraer sufijo desde la vocal tónica
    raw_suffix = w[tonic_index:]
    
    # 3. Quedarse SOLO con las vocales (ignorando consonantes para rima asonante)
    clean_vowels = "".join([c for c in raw_suffix if c in vowels])
    
    # 4. Normalizar tildes para la comparación (ó -> o)
    return clean_vowels.translate(str.maketrans("áéíóú", "aeiou"))

def has_rhyme(text: str) -> bool:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if len(lines) < 2:
        return False
    
    # Obtenemos los sufijos vocálicos de la última palabra de cada línea
    endings = []
    for line in lines:
        words = line.split()
        if words:
            endings.append(rhyme_suffix(words[-1]))
            
    # Comprobamos si hay al menos una coincidencia en los sufijos
    # (Usamos set para ver si se reduce la cantidad de elementos únicos)
    if not endings: return False
    return len(set(endings)) < len(endings)
    
def generate(topic: str) -> None:
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un rapero experto. Genera exactamente UN PAREADO (2 líneas) que rime entre sí. Solo el texto."},
                {"role": "user", "content": f"Tema: {topic}"}
            ],
            stream=False,
        )
        rap = resp.choices[0].message.content
        print(f"Rap generado:\n{rap}")
        print("RIMA APROBADA" if has_rhyme(rap) else "RIMA DESCARTADA")
        print()
    except Exception as e:
        print(f"Error API: {e}")

if __name__ == "__main__":
    for _ in range(10):
        generate("cualquier tema")
