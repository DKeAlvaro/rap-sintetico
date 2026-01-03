import random
from config import client_rhyme
from rhyme import has_rhyme
from constants import SEEDS

def generate_rhyme() -> dict | None:
    """Genera un pareado basado en un tema aleatorio."""
    topic = random.choice(SEEDS)
    
    try:
        resp = client_rhyme.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un rapero experto. Genera exactamente UN PAREADO (2 líneas) que rime entre sí. Solo el texto. Se creativo con el estilo."},
                {"role": "user", "content": f"Haz un rap sobre: {topic}"}
            ],
            stream=False,
        )
        rap = resp.choices[0].message.content
        is_valid = has_rhyme(rap)
        
        # Opcional: imprimir para debug si el usuario quiere, pero el tqdm limpia la pantalla
        # print(f"[{topic}] -> {rap}") 
        
        return {"topic": topic, "rap": rap} if is_valid else None
    except Exception as e:
        print(f"Error API Rima: {e}")
        return None
