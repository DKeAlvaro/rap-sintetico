import random
from config import client_rhyme
from rhyme import has_rhyme
from constants import SEEDS, STYLES

def generate_rhyme() -> dict | None:
    """Genera un pareado basado en un tema y estilo aleatorios."""
    topic = random.choice(SEEDS)
    style = random.choice(STYLES)
    context = f"Tema: {topic}. Estilo: {style}"
    
    try:
        resp = client_rhyme.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un rapero experto. Genera exactamente UN PAREADO (2 líneas) que rime entre sí. Solo el texto."},
                {"role": "user", "content": context}
            ],
            stream=False,
        )
        rap = resp.choices[0].message.content
        is_valid = has_rhyme(rap)
        # print()
        # print(f"[{context}]")
        # print(f"Rima:\n{rap}")
        # print("RIMA APROBADA" if is_valid else "RIMA DESCARTADA")
        # print()
        
        return {"topic": context, "rap": rap} if is_valid else None
    except Exception as e:
        print(f"Error API Rima: {e}")
        return None
