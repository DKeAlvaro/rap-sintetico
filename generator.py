import random
from config import client_rhyme, client_context
from rhyme import has_rhyme

SEEDS = [
    # Conceptos Generales
    "futuro distópico", "vida cotidiana", "barrio peligroso", "amor tóxico", 
    "comida chatarra", "viajes espaciales", "naturaleza salvaje", "fiesta desenfrenada",
    "dinero y lujo", "soledad urbana", "películas de terror", "deportes extremos",
    "teorías conspirativas", "alienígenas", "apocalipsis zombie", "inteligencia artificial",
    
    # Raperos y Figuras
    "Eminem", "Tupac", "Notorious B.I.G.", "Duki", "Wos", "Aczino", "Chuty", "Skone",
    "Residente", "Canserbero", "Daddy Yankee", "Snoop Dogg", "Jay-Z", "Kanye West",
    
    # Personajes Ficticios
    "Batman", "Joker", "Spiderman", "Goku", "Vegeta", "Naruto", "Luffy", "Darth Vader",
    "Harry Potter", "Walter White", "Tony Stark", "Homer Simpson", "Super Mario",
    
    # Marcas y Productos
    "Nike Air Jordan", "Adidas", "Supreme", "Gucci", "Rolex", "Ferrari", "Tesla",
    "McDonald's", "Coca-Cola", "iPhone", "PlayStation 5", "Netflix",
    
    # Lugares y Eventos
    "El Bronx", "Compton", "La Bombonera", "Torre Eiffel", "Marte", "Chernobyl",
    "Final del Mundial", "Super Bowl", "Tomorrowland", "Area 51",
    
    # Cultura Pop y Tendencias
    "Bitcoin", "NFTs", "TikTok", "Memes", "Haters", "Fake News", "Reggaeton antiguo",
    "Trap argentino", "Batalla de los Gallos", "FMS Internacional"
]

def generate_context() -> str:
    """Genera un contexto creativo (Tema + Estilo) usando el LLM local."""
    seed = random.choice(SEEDS)
    try:
        resp = client_context.chat.completions.create(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": "Eres un director creativo de batallas de rap. Genera un contexto MUY CORTO (máximo 15 palabras). Formato obligatorio: 'Tema: [X]. Estilo: [Y]'. Sin explicaciones extra."},
                {"role": "user", "content": f"Dame un contexto rápido para un rap. Inspírate en: {seed}"}
            ],
            stream=False,
            temperature=1.2 # Slightly higher temperature for more randomness
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generando contexto: {e}")
        return "Tema: Freestyle libre. Estilo: Clásico"

def generate_rhyme(topic: str) -> dict | None:
    """Genera un pareado basado en el tema y verifica si rima."""
    try:
        resp = client_rhyme.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un rapero experto. Genera exactamente UN PAREADO (2 líneas) que rime entre sí. Solo el texto."},
                {"role": "user", "content": f"{topic}"} # Topic variable already includes "Tema: ... Estilo: ..."
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
        print(f"Error API Rima: {e}")
        return None
