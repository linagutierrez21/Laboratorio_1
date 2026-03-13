char dato;

void setup() {
  Serial.begin(9600);

  pinMode(13, OUTPUT); // LED rojo
  pinMode(12, OUTPUT); // LED verde

  digitalWrite(13, LOW);
  digitalWrite(12, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    dato = Serial.read();

    // Apagar ambos LEDs antes de encender uno
    digitalWrite(13, LOW);
    digitalWrite(12, LOW);

    if (dato == 'R') {
      digitalWrite(13, HIGH); // rojo ON
    }
    else if (dato == 'V') {
      digitalWrite(12, HIGH); // verde ON
    }
  }
}