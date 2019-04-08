/*
 * Radio sender
 *
 */

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#include <button_radio.h>



/* ==[ VARIABLES ]== */
/* pins */
enum Pins
{
  PIN_CE  = 7,
  PIN_CSN = 8,
};

RF24 radio(PIN_CE, PIN_CSN);

/* radio addresses */
byte const my_name[6] = "NODE0";
byte const child_name[6] = "CHILD";



/* setup: initialization */
void setup()
{
  Serial.begin(9600);
  radio.begin();

  /* open writing pipe to child */
  radio.openWritingPipe(child_name);

  /* start listening on `my_name' */
  radio.openReadingPipe(1, my_name);

  /* radio configuration */
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
}

byte i = 0x00;
int delta = -8;

/* loop: main loop */
void loop()
{
  /* check if a message is available */
  while (radio.available())
  {
    char msg[32] = "";
    radio.read(&msg, sizeof(msg));
    Serial.print("Received '");
    Serial.print(msg);
    Serial.println("'");

    switch(msg[0])
    {
    case ID_INSTRUCTION:
      Serial.println("Instruction");
      break;
    case ID_BUTTON_EVENT:
      Serial.println("Button Event");
      ButtonEvent e;
      memcpy(&e, msg+1, sizeof(ButtonEvent));

      Serial.print("Team ");
      Serial.print(e.team);
      Serial.print(", player ");
      Serial.print(e.player);
      Serial.print(" @ ");
      Serial.print(e.time_ms);
      Serial.print("ms, ");
      Serial.print(e.time_us);
      Serial.println("us");
      break;
    }
  }

  Instruction inst(OP_WRITE_REGISTER);
  inst.data[0] = REG_SOUND;
  inst.data[1] = i;
  send_message(radio, child_name, inst);

  Instruction inst2(OP_NEW_QUESTION);
  send_message(radio, child_name, inst2);


  if (i == 0xFE || i == 0x00)
  { delta *= -1;
  }
  i += delta;

  delay(50);
}

