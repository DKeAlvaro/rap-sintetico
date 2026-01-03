import os, re, json
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
        is_valid = has_rhyme(rap)
        print(f"Rima:\n{rap}")
        print("RIMA APROBADA" if is_valid else "RIMA DESCARTADA")
        print()
        return {"topic": topic, "rap": rap} if is_valid else None
    except Exception as e:
        print(f"Error API: {e}")
        return None

import random

TOPICS = [
    "la vida en la calle",
    "el futuro de la tecnología",
    "un amor perdido",
    "la lucha por el éxito",
    "viajes espaciales",
    "la naturaleza salvaje",
    "mitología antigua",
    "el día a día en la oficina",
    "videojuegos retro",
    "la cocina de la abuela",
    "El Quinto Escalón",
    "Final de la FMS",
    "Batalla contra Arkano",
    "El flow de Chuty",
    "Aczino en la tarima",
    "Duki en la plaza",
    "Wos tirando rimas",
    "Red Bull Batalla de los Gallos",
    "Improvisación con objetos",
    "Minuto a sangre",
    "Doble tempo extremo",
    "Réplica injusta",
    "El jurado votó mal",
    "Leyendas del freestyle",
    "Cultura Hip Hop",
    "Graffiti en el tren",
    "Beatbox en la esquina"
]

STYLES = [
    "agresivo",
    "melancólico",
    "filosófico",
    "humorístico",
    "old school",
    "trap futurista",
    "poético",
    "sarcástico",
    "metriquer",
    "flow pesado",
    "doble tempo",
    "hardcore",
    "ingenioso",
    "competitivo",
    "a capella",
    "reggae vibe",
    "underground",
    "comercial"
]

if __name__ == "__main__":
    dataset_file = "dataset.jsonl"
    with open(dataset_file, "a", encoding="utf-8") as f:
        for _ in range(10):
            topic = random.choice(TOPICS)
            style = random.choice(STYLES)
            context = f"Tema: {topic}. Estilo: {style}"
            print(f"Contexto: {context}")
            result = generate(context)
            if result:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                f.flush()
    print(f"Dataset actualizado en {dataset_file}")
