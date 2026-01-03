import json
from config import DATASET_FILE, N_GENERATIONS
from generator import generate_rhyme
from tqdm import tqdm

def main():
    print("Iniciando generación aleatoria...")
    
    with open(DATASET_FILE, "a", encoding="utf-8") as f:
        for i in tqdm(range(N_GENERATIONS)):
            result = generate_rhyme()
            
            if result:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                f.flush()
                
    print(f"Dataset actualizado en {DATASET_FILE}")

if __name__ == "__main__":
    main()
