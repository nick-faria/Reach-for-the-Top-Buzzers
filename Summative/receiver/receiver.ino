/*
 * Button
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

uint16_t       this_node = 01;
uint16_t const parent    = 00;


bool can_be_pressed = true;

byte registers[REGISTER_COUNT];


/* ==[ FUNCTIONS ]== */
void interpret_message(RF24NetworkHeader header, byte *message);
bool pair(void);



void setup()
{
  Serial.begin(9600);
  radio.begin();
  radio.setDataRate(RF24_2MBPS);

  pinMode(PIN_LIGHT , OUTPUT);
  pinMode(PIN_BUTTON, INPUT_PULLUP);

  Serial.println("Pairing...");
  while (pair() == false)
  {
    delay(100);
  }
  Serial.println("Paired.");

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

    interpret_message(header, message);
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

  analogWrite(PIN_SOUND, registers[REG_SOUND]);
  digitalWrite(PIN_LIGHT, registers[REG_LIGHT]);
}

/* pair: pair the button with the server */
bool pair(void)
{
  /*  PAIRING PROCEDURE
   *  =================
   * connect to the server
   * ping the server until it acknowledges or until it times out
   * if we were acknowledged:
   *  set our address to the address received from the server
   *  ping the server again to verify our connection
   *  if it failed:
   *   goto begin.
   *  else:
   *    done.
   * else:
   *  goto begin.
   */

  // make sure we can actually talk to the server
  if (ping())
  {
    // Node 01 is reserved for pairing
    network.begin(01);

    // request to pair with the server
    RF24NetworkHeader pair_header(parent, ID_PAIR);
    char pair_msg[32] = "";
    network.write(pair_header, pair_msg, sizeof(pair_msg));

    // wait for the pairing message from the server
    while (!network.available())
    {
      network.update();
    }

    // receive our new address
    uint16_t address = 0;
    RF24NetworkHeader recv_header;
    network.read(recv_header, &address, sizeof(address));
    Serial.print("new address is ");
    Serial.println(address);

    // set our new address
    network.begin(address);
    this_node = address;

    // ensure we can connect to the server with our new address
    if (ping())
    {
      return true;
    }
  }
  // we were not acknowledged
  else
  {
    Serial.println("Server pong timed out!");
  }

  return false;
}

/* ping: ping the server */
bool ping(void)
{
  return true;
  unsigned long PING_TIMEOUT = 10000;

  // try to ping the server
  RF24NetworkHeader ping_header(parent, ID_PING);
  char ping[32] = "ping";
  network.write(ping_header, ping, sizeof(ping));
  Serial.println("Ping!");

  unsigned long start = millis();


  // wait for the pong from the server
  while (!network.available())
  {
    network.update();
    if (millis() - start > PING_TIMEOUT)
    {
      return false;
    }
  }

  // receive the pong from the server
  RF24NetworkHeader pong_header;
  char pong[32];
  network.read(pong_header, pong, sizeof(pong));

  return true;
}

