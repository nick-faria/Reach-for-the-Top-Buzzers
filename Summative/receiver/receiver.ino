/*
 *                            THE BUTTONS
 *                            ===========
 *
 *   There are 8 buttons. Each button is tied to a certain team, where
 * each team can have 4 buttons. The buttons each have an LED and a
 * piezo buzzer, which are controlled by the server. When the button is
 * pressed, it will send a message to the server. After the button has
 * been pressed, it will not send another event to the server until it
 * receives a "new question" message from the server.
 *
 */

/* TODO:
 *  - Add the piezo buzzer instead of just an oscillating LED
 *  - Add a button to start the pairing process
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

  PIN_BUTTON   = 5,
  PIN_PAIR_BTN = 4,
};


RF24 radio(PIN_CE, PIN_CSN);
RF24Network network(radio);

uint16_t       this_node = 01;
uint16_t const parent    = 00;


bool can_be_pressed = true;
int  pair_btn_previous = HIGH;

byte registers[REGISTER_COUNT];


/* ==[ FUNCTIONS ]== */
void interpret_message(RF24NetworkHeader header, byte *message);
bool pair(void);



void setup()
{
  Serial.begin(9600);
  radio.begin();
  radio.setDataRate(RF24_2MBPS);

  pinMode(PIN_LIGHT   , OUTPUT);
  pinMode(PIN_BUTTON  , INPUT_PULLUP);
  pinMode(PIN_PAIR_BTN, INPUT_PULLUP);

  Serial.println("Pairing...");
  while (pair() == false)
  {
    delay(1000);
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
    can_be_pressed = false;
    RF24NetworkHeader header(parent, ID_BUTTON_EVENT);

    ButtonEvent btn_event(0, 0);
    int msg_size = 0;
    byte *msg = btn_event.to_message(&msg_size);

    network.write(header, msg, msg_size);
    delayMicroseconds(300);
    delete[] msg;
    Serial.println("button pressed");
  }

  // whenever the pairing button is pressed, attempt to pair
  int pair_btn_state = digitalRead(PIN_PAIR_BTN);
  if (pair_btn_state == LOW && pair_btn_previous == HIGH)
  {
    uint16_t previous_address = this_node;
    if (!pair())
    {
      Serial.println("Failed to pair!");
      this_node = previous_address;
      network.begin(this_node);
    }
  }
  pair_btn_previous = pair_btn_state;

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

  digitalWrite(PIN_LIGHT, registers[REG_LIGHT]);
  analogWrite(PIN_SOUND, registers[REG_SOUND]);
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

  // send a disconnect message to the current parent, to make sure our old name is freed
  RF24NetworkHeader discon_header(parent, ID_DISCONNECT);
  byte discon_msg[32] = "";
  network.write(discon_header, discon_msg, sizeof(discon_msg));
  delay(50);

  // Node 01 is reserved for pairing
  network.begin(01);

  // make sure there is a server to pair with
  if (ping())
  {
    Serial.println("requesting new address!");

    // request to pair with the server
    RF24NetworkHeader pair_header(parent, ID_PAIR);
    char pair_msg[32] = "";
    network.write(pair_header, pair_msg, sizeof(pair_msg));

    // wait for the pairing message from the server
    bool got_pair_response = true;
    unsigned long const PAIRING_TIMEOUT = 1000;
    unsigned long pairing_begin = millis();
    network.update();
    while (!network.available())
    {
      Serial.println(millis() - pairing_begin);
      if (millis() - pairing_begin > PAIRING_TIMEOUT)
      {
        got_pair_response = false;
        break;
      }
      network.update();
    }

    if (got_pair_response)
    {
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
      else
      {
        Serial.println("Didn't receive pong after setting new address");
      }
    }
    else
    {
      Serial.println("Didn't receive new address");
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
  unsigned long const PING_TIMEOUT = 1000;

  // try to ping the server
  RF24NetworkHeader ping_header(parent, ID_PING);
  char ping[32] = "ping";
  network.write(ping_header, ping, sizeof(ping));
  Serial.println("Ping!");

  unsigned long start = millis();


  // wait for the pong from the server
  network.update();
  while (!network.available())
  {
    network.update();
    if (millis() - start > PING_TIMEOUT)
    {
      Serial.println("ping() -- didn't receive a pong");
      return false;
    }
  }

  // receive the pong from the server
  RF24NetworkHeader pong_header;
  char pong[32];
  network.read(pong_header, &pong, sizeof(pong));

  Serial.println("ping() -- got a pong");
  return true;
}

