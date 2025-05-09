// WEMOS D1 mini Lite
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "ALPRIME";
const char* password = "Techno0255";
const char* mqtt_server = "mqtt.dealgate.ru";
const char* mqtt_user = "alprime"; // Укажите ваш логин для MQTT
const char* mqtt_password = "Techno0255"; // Укажите ваш пароль для MQTT

WiFiClient espClient;
PubSubClient client(espClient);

const int ledPin = LED_BUILTIN;

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  reconnect();
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Подключение к MQTT брокеру с логином и паролем
    if (client.connect("WemosClient", mqtt_user, mqtt_password)) {
      Serial.println("connected");
      client.subscribe("train"); // Подписка на топик "train"
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("]: ");

  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  // Управление встроенным светодиодом
  if (String(topic) == "train") {
    if (message == "1") {
      digitalWrite(ledPin, LOW); // Включить светодиод
    } else if (message == "0") {
      digitalWrite(ledPin, HIGH); // Выключить светодиод
    }
  }
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
