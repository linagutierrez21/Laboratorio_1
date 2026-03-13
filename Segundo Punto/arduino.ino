#include <DHT.h>

const int led1Pin = 2;
const int led2Pin = 3;

#define DHTPIN 4       // pin de datos del DHT11 (DIGITAL)
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  digitalWrite(led1Pin, LOW);
  digitalWrite(led2Pin, LOW);

  Serial.begin(9600);
  dht.begin();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "LED1_ON") { digitalWrite(led1Pin, HIGH); Serial.println("OK: LED1 Encendido"); }
    else if (command == "LED1_OFF") { digitalWrite(led1Pin, LOW); Serial.println("OK: LED1 Apagado"); }
    else if (command == "LED2_ON") { digitalWrite(led2Pin, HIGH); Serial.println("OK: LED2 Encendido"); }
    else if (command == "LED2_OFF") { digitalWrite(led2Pin, LOW); Serial.println("OK: LED2 Apagado"); }
    else if (command == "GET_TEMP") {
      float t = dht.readTemperature(); // Celsius
      if (isnan(t)) Serial.println("ERR");
      else Serial.println((int)t);     // DHT11 suele ser entero
    }
  }
}