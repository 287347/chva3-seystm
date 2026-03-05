import os
import random
import string
import requests
import base64

# Configurazione dai "Secrets" di GitHub
TOKEN = os.getenv("GH_TOKEN")
REPO = "287347/chva3.seystm"
FILE_PATH = "key.txt"  # Il nome del file raw
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def update_github_file():
    # 1. Genera una chiave casuale di 20 caratteri
    chars = string.ascii_letters + string.digits
    new_key = ''.join(random.choices(chars, k=20))
    
    # 2. Ottieni lo 'SHA' del file attuale (necessario per sovrascriverlo)
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {TOKEN}"}
    
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha', None) # Se il file non esiste, sha sarà None

    # 3. Prepara il caricamento
    content_base64 = base64.b64encode(new_key.encode()).decode()
    data = {
        "message": "Aggiornamento automatico chiave",
        "content": content_base64,
        "sha": sha
    }

    # 4. Invia l'aggiornamento a GitHub
    put_response = requests.put(url, headers=headers, json=data)
    
    if put_response.status_code in [200, 201]:
        print(f"Chiave aggiornata con successo: {new_key}")
        # 5. Invia al Webhook di Discord
        payload = {
            "embeds": [{
                "title": "🔑 Chiave Script Aggiornata",
                "description": f"La nuova chiave valida per le prossime 24h è:\n\n`{new_key}`",
                "color": 3447003
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
    else:
        print("Errore nell'aggiornamento:", put_response.text)

if __name__ == "__main__":
    update_github_file()
