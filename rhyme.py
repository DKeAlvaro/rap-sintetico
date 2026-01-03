
def rhyme_suffix(word: str) -> str:
    """Extrae la terminación vocálica tónica para comprobar rima asonante."""
    w = word.lower().strip(".,;:!?'\"-")
    if not w: return ""

    vowels = "aeiouáéíóú"
    v_indices = [i for i, char in enumerate(w) if char in vowels]
    if not v_indices: return ""

    tonic_index = -1
    for i in v_indices:
        if w[i] in "áéíóú":
            tonic_index = i
            break
            
    if tonic_index == -1:
        last_char = w[-1]
        if last_char in "aeiouns":
            tonic_index = v_indices[-2] if len(v_indices) >= 2 else v_indices[-1]
        else:
            tonic_index = v_indices[-1]

    raw_suffix = w[tonic_index:]
    clean_vowels = "".join([c for c in raw_suffix if c in vowels])
    return clean_vowels.translate(str.maketrans("áéíóú", "aeiou"))

def has_rhyme(text: str) -> bool:
    """Comprueba si las últimas palabras de cada línea riman entre sí."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if len(lines) < 2: return False
    
    endings = []
    for line in lines:
        words = line.split()
        if words: endings.append(rhyme_suffix(words[-1]))
            
    if not endings: return False
    return len(set(endings)) < len(endings)
