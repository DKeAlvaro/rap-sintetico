import json
from config import DATASET_FILE
from generator import generate_context, generate_rhyme

def main():
    print("Iniciando generación con Doble LLM...")
    
    with open(DATASET_FILE, "a", encoding="utf-8") as f:
        for i in range(10):
            # Paso 1: Generar Contexto
            context = generate_context()
            print(f"[{i+1}/10] Contexto (LLM 1): {context}")
            
            # Paso 2: Generar Rima (LLM 2)
            result = generate_rhyme(context)
            
            if result:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                f.flush()
                
    print(f"Dataset actualizado en {DATASET_FILE}")

if __name__ == "__main__":
    main()
