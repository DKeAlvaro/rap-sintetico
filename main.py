import os, re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

VOWELS = "aeoáéóiuíúü"

def rhyme_suffix(word: str) -> str:
    w = word.lower().strip(".,;:!?'\"")
    if not w:
        return ""
    # Handle accented vowels
    if any(c in "áéíóú" for c in w):
        m = re.search(r'[áéíóú].*', w)
        return m.group(0).translate(str.maketrans("áéíóú", "aeiou")) if m else ""
    # Determine stress pattern
    is_llana = w[-1] in VOWELS + "ns"
    indices = [i for i, ch in enumerate(w) if ch in VOWELS]
    if not indices:
        return w
    start = indices[-2] if is_llana and len(indices) >= 2 else indices[-1]
    return w[start:]

def has_rhyme(text: str) -> bool:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if len(lines) < 2:
        return False
    endings = [rhyme_suffix(line.split()[-1]) for line in lines]
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
    except Exception as e:
        print(f"Error API: {e}")

if __name__ == "__main__":
    for _ in range(10):
        generate("cualquier tema")
