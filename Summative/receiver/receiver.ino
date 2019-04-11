/*
 * Radio receiver
 *
 */

#include <stdarg.h>

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#include <button_radio.h>



/* ==[ VARIABLES ]== */
int my_team = 0,
    my_player_number = 0;

bool can_be_pressed = true;

/* pins */
enum Pins
{
  PIN_CE  = 7,
  PIN_CSN = 8,

  PIN_LIGHT = 2,
  PIN_SOUND = 3,

  PIN_BUTTON = 5,
};

RF24 radio(PIN_CE, PIN_CSN);

/* radio addresses */
byte const my_name[6] = "CHILD";
byte const parent_name[6] = "NODE0";

/* registers */
byte registers[REGISTER_COUNT];

/* max number of events to process per loop */
unsigned const EVENTS_PER_LOOP = 16;



/* setup: initialization */
void setup()
{
  Serial.begin(9600);
  radio.begin();

  /* open writing pipe to parent */
  radio.openWritingPipe(parent_name);

  /* start listening on `my_name'*/
  radio.openReadingPipe(1, my_name);

  /* radio configuration */
  radio.setPALevel(RF24_PA_MIN);
  radio.setAutoAck(true);
  radio.setRetries(0,15);

  radio.startListening();

  Serial.println("Initialized");

  pinMode(PIN_LIGHT, OUTPUT);
  pinMode(PIN_BUTTON, INPUT_PULLUP);
}

/* loop: main loop */
void loop()
{
  /* if we've received a message, we must interpret it */
  for (unsigned i = 0; i < EVENTS_PER_LOOP && radio.available(); ++i)
  {
    /* read a message */
    byte message[32];
    radio.read(message, sizeof(message));
    byte id = message[0];

    switch (id)
    {
    /* instruction */
    case ID_INSTRUCTION:
     {
      byte opcode = message[1];
      switch (opcode)
      {
      /* mark a new question */
      case OP_NEW_QUESTION:
       {Serial.println("New Question");
        can_be_pressed = true;
       }break;

      /* write to a register */
      case OP_WRITE_REGISTER:
       {byte reg   = message[2],
             value = message[3];

        Serial.print("write 0x");
        Serial.print(value, HEX);
        Serial.print(" to register 0x");
        Serial.println(reg, HEX);

        registers[reg] = value;
       }break;
      
      default:
        error("unknown opcode %.2hhX", opcode);
        break;
      }
     }break;

    /* button event */
    case ID_BUTTON_EVENT:
     {Serial.println("Button Event");
      // TODO
     }break;

    default:
      Serial.println("error!");
      error("unknown message ID 0x%.2hhX", id);
      break;
    }
  }


  /* detect events on this button */
  if (digitalRead(PIN_BUTTON) == LOW)
  {
    if (can_be_pressed)
    {
      Serial.println("button is pressed!");
      ButtonEvent event(my_team, my_player_number);

      while (send_message(radio, parent_name, event) == false)
      {
      }
      can_be_pressed = false;
    }
  }


  /* turn on light, sound buzzer, etc. if we are told to */
  digitalWrite(PIN_LIGHT, registers[REG_LIGHT] & 0x01);
  analogWrite(PIN_SOUND, registers[REG_SOUND]);

  Serial.println("End of Cycle\n");
}

