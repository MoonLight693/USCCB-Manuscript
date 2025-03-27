import google.generativeai as genai
import config

def list_available_models():
    # List all available models and their supported methods
    models = genai.list_models()
    for model in models:
        print(f"Model ID: {model.name}")
        print(f"Supported Methods: {model.supported_generation_methods}")
        print("-" * 40)

# Example usage:
# Uncomment the line below to list models when running the script
genai.configure(api_key=config.API_KEY)

list_available_models()
