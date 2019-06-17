bool Pressed = false;
int first,Press = 0;
int Line =125;
bool Rea,dable[8] = {true, true, true, true, true, true, true, true};
int  PINS [8] = {4, 5, 6, 7, 10, 11, 12, 13};
void setup() {
  pinMode(4, INPUT_PULLUP);  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);  pinMode(7, INPUT_PULLUP);
  pinMode(13, INPUT_PULLUP);  pinMode(12, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);  pinMode(10, INPUT_PULLUP);
  Serial.begin(9600);
}
void loop() {
  if (Pressed) {
    Serial.println(Press);
  }
  else {
    Press = 8;
    for (int X = 0; X < 8; X++) {
      int J = Read(PINS[X]);
      if (J) {
        Press = X;
      }
    }
    if (bitRead(Line, Press)) {
      Pressed = true;
      first = Press;
      Write(Press, true);
      Serial.println(first);
    }
  }
  if (Serial.available()) {
    Line = Serial.read();
    Pressed = false;
  }
}
void Write(int Slave, bool State) {
}
int Read(int Num) {
  return (!digitalRead(Num));
}
