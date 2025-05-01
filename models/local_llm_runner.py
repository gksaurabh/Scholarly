import subprocess
import json

def query_ollama(prompt, model="mistral", system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    command = [
        "ollama", "run", model,
        json.dumps({"messages": messages})
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        return "⚠️ Error running Ollama"

    try:
        output = result.stdout.strip().split("\n")[-1]
        return output
    except Exception:
        return "⚠️ Failed to parse LLM output"
