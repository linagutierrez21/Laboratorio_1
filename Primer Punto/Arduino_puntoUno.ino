// Entradas DIP (binario)
int A = 2;
int B = 3;
int C = 4;
int D = 5;

// Display de decenas
int decenasSeg[] = {6,7,8,9,10,11,12};

// Display de unidades
int unidadesSeg[] = {A0,A1,A2,A3,A4,A5,13};

// Tabla números 0-9 (cátodo común)
byte numeros[10][7] = {
  {1,1,1,1,1,1,0}, // 0
  {0,1,1,0,0,0,0}, // 1
  {1,1,0,1,1,0,1}, // 2
  {1,1,1,1,0,0,1}, // 3
  {0,1,1,0,0,1,1}, // 4
  {1,0,1,1,0,1,1}, // 5
  {1,0,1,1,1,1,1}, // 6
  {1,1,1,0,0,0,0}, // 7
  {1,1,1,1,1,1,1}, // 8
  {1,1,1,1,0,1,1}  // 9
};

void setup() {
  // Entradas con pull-up interno
  pinMode(A, INPUT_PULLUP);
  pinMode(B, INPUT_PULLUP);
  pinMode(C, INPUT_PULLUP);
  pinMode(D, INPUT_PULLUP);

  // Salidas displays
  for(int i=0;i<7;i++){
    pinMode(decenasSeg[i], OUTPUT);
    pinMode(unidadesSeg[i], OUTPUT);
  }
}

void loop() {

  // Leer DIP (invertido por pull-up)
  int a = !digitalRead(A);
  int b = !digitalRead(B);
  int c = !digitalRead(C);
  int d = !digitalRead(D);

  // Convertir binario a decimal
  int decimal = d*8 + c*4 + b*2 + a;

  // Separar decenas y unidades
  int decenas = decimal / 10;
  int unidades = decimal % 10;

  // Mostrar en displays
  mostrar(decenasSeg, decenas);
  mostrar(unidadesSeg, unidades);
}

// Función para mostrar número
void mostrar(int display[], int num){
  for(int i=0;i<7;i++){
    digitalWrite(display[i], numeros[num][i]);
  }
}
