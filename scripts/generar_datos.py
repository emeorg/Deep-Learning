import requests
import json
import os

# Configuracion general
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELOS = ["llama3.2:3b", "phi3:mini", "mistral:7b"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT_FILE = os.path.join(BASE_DIR, "prompts", "prompts.md")
OUTPUT_DIR = os.path.join(BASE_DIR, "datasets")
ITERACIONES_POR_MODELO = 5

def initialize_environment(output_directory):
    os.makedirs(output_directory, exist_ok=True)

def read_base_prompt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: No se pudo localizar el archivo de prompt en {file_path}")
        return None

def create_dynamic_prompt(base_prompt, iteration_number):
    instruction = (
        f"\n\n[Instrucción del sistema: Esta es la iteración número {iteration_number}. "
        "Es estrictamente necesario que generes ejemplos completamente distintos a los de las "
        "iteraciones anteriores. Mantén la estructura JSON solicitada.]"
    )
    return base_prompt + instruction

def fetch_model_response(model_name, prompt):
    payload = {
        "model": model_name,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.85,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        print(f"Error de red o API al consultar {model_name}: {e}")
        return None

def parse_json_response(response_text):
    if not response_text:
        return None
        
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return None

def append_to_jsonl(file_path, data):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")

def get_output_filepath(output_dir, model_name):
    safe_name = model_name.replace(":", "_")
    return os.path.join(output_dir, f"{safe_name}_dataset.jsonl")

def generate_data_for_model(model, base_prompt):
    print(f"\n--- Iniciando recoleccion de datos con el modelo: {model} ---")
    output_filepath = get_output_filepath(OUTPUT_DIR, model)
    
    for iteration in range(1, ITERACIONES_POR_MODELO + 1):
        print(f"  Procesando iteracion {iteration}...")
        
        prompt = create_dynamic_prompt(base_prompt, iteration)
        raw_response = fetch_model_response(model, prompt)
        parsed_data = parse_json_response(raw_response)
        
        if parsed_data is not None:
            append_to_jsonl(output_filepath, parsed_data)
            print(f"  Exito: Datos de la iteracion {iteration} guardados correctamente.")
        else:
            print(f"  Advertencia: La iteracion {iteration} produjo un formato invalido o vacio. Se ha omitido.")

def run_pipeline():
    print("Iniciando el pipeline de generacion de datos sinteticos.")
    
    initialize_environment(OUTPUT_DIR)
    
    base_prompt = read_base_prompt(PROMPT_FILE)
    if base_prompt is None:
        print("Operacion abortada debido a que no se encontro el prompt base.")
        return

    for model in MODELOS:
        generate_data_for_model(model, base_prompt)

    print("\nProceso finalizado. Los datasets generados se encuentran en el directorio de salida.")

if __name__ == "__main__":
    run_pipeline()