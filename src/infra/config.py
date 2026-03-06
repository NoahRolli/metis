import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
    MQTT_USER = os.getenv("MQTT_USER")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
    
    CA_CERTS_PATH = "infra/mosquitto/certs/ca.crt"
    OLLAMA_URL = os.getenv("OLLAMA_URL")

    @classmethod
    def validate(cls):
        if not cls.MQTT_USER or not cls.MQTT_PASSWORD:
            raise ValueError("Sicherheitsleck: MQTT-Zugangsdaten fehlen in der .env Datei.")