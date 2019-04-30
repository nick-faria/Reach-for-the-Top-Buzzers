long Elap=1;
int len=2;
String X;
int J;
int Y=0;
bool LOOP=true;
void setup() {
  // put your setup code here, to run once:
  pinMode(13,OUTPUT);
Serial.begin(9600);
Serial.setTimeout(50);
Serial.print("HAM");
while(LOOP==true){
  if (Serial.available()){
LOOP=false;
}
}
}


void loop() {
  long Cur=millis()-Elap;
  // put your main code here, to run repeatedly:
//String X=Serial.read();

if (Serial.available()){
X=Serial.readStringUntil('/n');
String F=("33");
for (int K=0;K<len;K++){
Serial.print((X[0]));
}//Serial.flush();
Y+=1;
//digitalWrite(13,HIGH);

}
if (Cur>1500){
//Serial.println(X);
Elap=millis();
//Y+=1;
}

}//}


/* ser = serial.Serial()
>>> ser.baudrate = 19200
>>> ser.port = 'COM1'
>>> ser
Serial<id=0xa81c10, open=False>(port='COM1', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
>>> ser.open()
>>> ser.is_open
True
>>> ser.close()
>>> ser.is_open
False */ 

