import requests
from src.infra.config import Config

class AIService:
    """
    Dienst zur Kommunikation mit der lokalen Ollama-Instanz.
    Kapselt die gesamte Logik für API-Aufrufe an das Sprachmodell.
    """

    def __init__(self, model_name="llama3"):
        """
        Initialisiert den AI-Service mit der Konfiguration aus dem Environment.
        
        :param model_name: Name des Modells, das in Ollama verwendet wird (Standard: llama3).
        """
        self.url = Config.OLLAMA_URL
        self.model = model_name

    def generate_response(self, prompt: str) -> str:
        """
        Sendet einen synchronen Request an das LLM und extrahiert die Antwort.
        
        :param prompt: Die Eingabe (Frage/Anweisung) für das Modell.
        :return: Die generierte Textantwort als String oder eine Fehlermeldung bei Abbruch.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False  # Wir warten auf die komplette Antwort, kein Streaming
        }
        
        try:
            # HTTP POST Request an die Ollama API senden (Timeout nach 30 Sekunden)
            response = requests.post(self.url, json=payload, timeout=30)
            
            # Wirft eine Exception, falls der HTTP-Statuscode einen Fehler anzeigt (z.B. 404, 500)
            response.raise_for_status()
            
            # Die JSON-Antwort parsen und den reinen Text extrahieren
            data = response.json()
            return data.get("response", "")
            
        except requests.exceptions.RequestException as e:
            # Sauberes Error-Handling, damit das System bei einem Ollama-Ausfall nicht abstürzt
            error_msg = f"Fehler bei der Kommunikation mit dem Sprachmodell: {e}"
            print(f"[Metis AI] {error_msg}")
            return error_msg