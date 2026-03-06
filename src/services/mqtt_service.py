import ssl
import paho.mqtt.client as mqtt
from src.infra.config import Config

class MQTTService:
    def __init__(self, client_id="metis_core"):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self.client.username_pw_set(Config.MQTT_USER, Config.MQTT_PASSWORD)
        
        self.client.tls_set(
            ca_certs=Config.CA_CERTS_PATH,
            tls_version=ssl.PROTOCOL_TLSv1_3
        )
        
        self.client.on_connect = self._on_connect
        self.client.on_publish = self._on_publish

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("[Metis Network] Verschlüsselte Verbindung zum Broker etabliert.")
        else:
            print(f"[Metis Network] Verbindungsfehler. Code: {reason_code}")

    def _on_publish(self, client, userdata, mid, reason_code, properties):
        pass # Stilles Logging, um die Konsole nicht zu spammen

    def connect_and_start(self):
        try:
            self.client.connect(Config.MQTT_BROKER, Config.MQTT_PORT)
            self.client.loop_start()
        except Exception as e:
            print(f"[Metis Network] Fataler Fehler beim Verbindungsaufbau: {e}")

    def send_system_status(self, status_message):
        topic = "metis/system/status"
        self.client.publish(topic, status_message, qos=1)
        
    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("[Metis Network] Verbindung sicher getrennt.")