/*
 * thing
 *
 */

#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>

#include <button_radio.h>


/* ==[ VARIABLES ]== */
/* pins */
enum
{
  PIN_CE  = 7,
  PIN_CSN = 8,

  PIN_LIGHT = 2,
  PIN_SOUND = 3,

  PIN_BUTTON = 5,
};


RF24 radio(PIN_CE, PIN_CSN);
RF24Network network(radio);

#define SECOND  0

#if SECOND
const uint16_t this_node = 02;
#else
const uint16_t this_node = 01;
#endif
const uint16_t parent    = 00;


bool can_be_pressed = true;

byte registers[REGISTER_COUNT];


/* ==[ FUNCTIONS ]== */
void interpret_message(RF24NetworkHeader header, byte *message);



void setup()
{
  Serial.begin(9600);
  radio.begin();
  network.begin(this_node);
  radio.setDataRate(RF24_2MBPS);

  pinMode(PIN_LIGHT , OUTPUT);
  pinMode(PIN_BUTTON, INPUT_PULLUP);

  Serial.println("Initialized");
}

void loop()
{
  network.update();

  /* receive messages */
  while (network.available())
  {
    /* read the message from the network */
    RF24NetworkHeader header;
    char message[32];
    Serial.println("Reading...");
    network.read(header, &message, 32);
    Serial.print("Received ");
    Serial.println(message);

    /* interpret the message */
    interpret_message(header, message);

    network.update();
  }

  if (digitalRead(PIN_BUTTON) == LOW)
  {
    RF24NetworkHeader header(parent, ID_BUTTON_EVENT);

    ButtonEvent btn_event(0, 0);
    int msg_size = 0;
    byte *msg = btn_event.to_message(&msg_size);

    network.write(header, msg, msg_size);
    delete[] msg;
    Serial.println("button pressed");
  }

  delay(50);
}



/* intepret_message: interpret a message from the network */
void interpret_message(RF24NetworkHeader header, byte *message)
{
  switch(header.type)
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
    error("unknown message ID 0x%.2hhX", header.type);
    break;
  }
}

