import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
LOCAL_LLM_URL = "http://localhost:52625/v1"

# Client for generating rhymes (DeepSeek)
client_rhyme = OpenAI(
    api_key=DEEPSEEK_API_KEY, 
    base_url="https://api.deepseek.com"
)

# Client for generating contexts (Local Llama)
client_context = OpenAI(
    api_key="FLM", 
    base_url=LOCAL_LLM_URL
)

DATASET_FILE = "dataset.jsonl"
