import time
from src.infra.config import Config
from src.services.mqtt_service import MQTTService

def main():
    Config.validate()
    print("Metis Core initialisiert. Starte Subsysteme...")

    network = MQTTService()
    network.connect_and_start()

    time.sleep(1)
    network.send_system_status("MacBook M3 (Metis Core) ist online und gesichert.")

    try:
        print("System läuft. Drücke CTRL+C zum Beenden.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutdown-Signal empfangen.")
    finally:
        network.stop()

if __name__ == "__main__":
    main()