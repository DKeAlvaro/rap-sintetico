import json
from config import DATASET_FILE, N_GENERATIONS
from generator import generate_rhyme

def main():
    print("Iniciando generación aleatoria (Single LLM)...")
    
    with open(DATASET_FILE, "a", encoding="utf-8") as f:
        for i in range(N_GENERATIONS):
            print(f"[{i+1}/{N_GENERATIONS}] Generando...")
            result = generate_rhyme()
            
            if result:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                f.flush()
                
    print(f"Dataset actualizado en {DATASET_FILE}")

if __name__ == "__main__":
    main()
