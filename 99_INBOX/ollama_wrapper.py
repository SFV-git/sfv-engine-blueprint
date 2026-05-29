"""
SFV ENGINE — OLLAMA WRAPPER
Calls local Ollama model with SFV context.
Usage: python ollama_wrapper.py "your task prompt here"
Run 'ollama serve' in a terminal tab before using this.
"""

import requests
import json
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:14b"

SFV_SYSTEM_PROMPT = """You are a task assistant for SFV Engine, a photography production system.
Branches: MYTHOLOGY, LIVE, EVENTS, ATHLETICS, STUDIO, UGC, ARCHIVE, WORLD, 404
Revenue: UGC content retainers + EVENTS on-site portraits
Your role: handle specific low-value tasks. Never make creative decisions.
If unsure, say UNSURE. Output exactly what is asked. No extra commentary."""

def ask_ollama(task_prompt, system=SFV_SYSTEM_PROMPT, model=MODEL):
    full_prompt = f"{system}\n\nTASK:\n{task_prompt}"
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": full_prompt, "stream": False},
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        return "ERROR: Ollama not running. Run 'ollama serve' in terminal first."
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ollama_wrapper.py 'your prompt here'")
        sys.exit(1)
    prompt = " ".join(sys.argv[1:])
    result = ask_ollama(prompt)
    print(result)

# CONNECTED FILES
# - [[OLLAMA_SETUP|Ollama Setup]]
# - [[OLLAMA_PROMPTS|Ollama Prompts]]
# - [[MODEL_ROUTING|Model Routing]]
# - [[AI_USE_CASE_PROFILE|AI Use Case Profile]]
