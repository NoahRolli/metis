import time
from src.infra.config import Config
from src.services.mqtt_service import MQTTService
from src.services.ai_service import AIService

def main():
    # 1. Konfiguration prüfen
    Config.validate()
    print("Metis Core initialisiert. Starte Subsysteme...")

    # 2. Netzwerk-Service (MQTT) instanziieren und starten
    network = MQTTService()
    network.connect_and_start()

    # 3. AI-Service (Ollama) instanziieren
    # Wichtig: Falls du ein anderes Modell als 'llama3' lokal gezogen hast, 
    # passe den Namen hier entsprechend an (z.B. 'mistral' oder 'phi3').
    ai = AIService(model_name="llama3")

    # Dem Broker eine Sekunde Zeit für den TLS-Handshake geben
    time.sleep(1)
    network.send_system_status("MacBook M3 (Metis Core) ist online und gesichert.")

    # 4. Den ersten kognitiven Test durchführen
    print("[Metis Core] Wecke das Sprachmodell auf. Sende Test-Prompt...")
    test_prompt = "Antworte in einem kurzen, prägnanten Satz: Bist du online und bereit, Daten zu verarbeiten?"
    
    # Antwort von Ollama generieren lassen
    ai_response = ai.generate_response(test_prompt)
    print(f"[Metis AI] {ai_response}")
    
    # Die KI-Antwort direkt sicher über das MQTT-Netzwerk schicken
    network.send_system_status(f"System Check (AI): {ai_response}")

    # 5. Endlosschleife für den Dauerbetrieb
    try:
        print("System läuft und hört ab jetzt zu. Drücke CTRL+C zum Beenden.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Metis Core] Shutdown-Signal empfangen. Fahre Systeme herunter...")
    finally:
        network.stop()

if __name__ == "__main__":
    main()