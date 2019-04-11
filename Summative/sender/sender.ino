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


/* ==[ FUNCTIONS ]== */
void receive_messages(void);



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
  radio.setAutoAck(true);
  radio.setRetries(0,15);

  radio.startListening();
}

byte i = 0x00;
int delta = -8;

/* loop: main loop */
void loop()
{
  /* check if a message is available */
  unsigned long start = millis();
  while (millis() - start < 50)
  { receive_messages();
  }

  Instruction inst(OP_WRITE_REGISTER);
  inst.data[0] = REG_SOUND;
  inst.data[1] = i;
  bool success = send_message(radio, child_name, inst);
  Serial.print(success);

  if (i == 0xFE || i == 0x00)
  { delta *= -1;
  }
  i += delta;
}

/* receive_messages:  */
void receive_messages(void)
{
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

      Instruction inst2(OP_NEW_QUESTION);
      while (send_message(radio, child_name, inst2) == false)
      {
      }
      break;
    }
  }
}

