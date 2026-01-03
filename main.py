import json
from config import DATASET_FILE, N_GENERATIONS
from generator import generate_rhyme
from tqdm import tqdm

def main():
    print("Iniciando generación aleatoria...")
    
    valid_count = 0
    pbar = tqdm(range(N_GENERATIONS))
    
    with open(DATASET_FILE, "a", encoding="utf-8") as f:
        for i in pbar:
            result = generate_rhyme()
            
            if result:
                valid_count += 1
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                f.flush()
            
            accuracy = (valid_count / (i + 1)) * 100
            pbar.set_postfix({"Aprobadas": f"{accuracy:.1f}%"})
                
    print(f"Dataset actualizado en {DATASET_FILE}")

if __name__ == "__main__":
    main()
