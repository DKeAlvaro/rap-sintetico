import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import DATASET_FILE, N_GENERATIONS
from generator import generate_rhyme
from tqdm import tqdm

def main():
    print(f"Iniciando generación paralela ({N_GENERATIONS} peticiones)...")
    
    valid_count = 0
    
    # Paralelizamos las llamadas a la API (I/O bound)
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(generate_rhyme) for _ in range(N_GENERATIONS)]
        
        with open(DATASET_FILE, "a", encoding="utf-8") as f:
            pbar = tqdm(as_completed(futures), total=N_GENERATIONS)
            
            for i, future in enumerate(pbar):
                result = future.result()
                
                if result:
                    valid_count += 1
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")
                    f.flush()
                
                accuracy = (valid_count / (i + 1)) * 100
                pbar.set_postfix({"Aprobadas": f"{accuracy:.1f}%"})
                
    print(f"Dataset actualizado en {DATASET_FILE}")

if __name__ == "__main__":
    main()
