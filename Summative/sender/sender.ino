/*
 *                            THE SERVER
 *                            ==========
 *
 *   The server is the central hub. This is where all the buttons
 * send their event data, and where the computer sends out its
 * instructions to the buttons. When the server receives an event
 * message from the buttons, it passes it up to the computer. In
 * turn, the computer sends instructions down to the server to be
 * sent out to the buttons.
 *
 */

/* TODO:
 *  - Send button presses to the computer
 *  - Add a button to start the pairing process
 *  - Start using the Arduino Mega
 *   (NOTE -- you seemingly can't change which pins are used for
 *    SPI, rendering the Mega pointless)
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

  PIN_PAIR_BTN = 5,
};


RF24 radio(PIN_CE, PIN_CSN);
RF24Network network(radio);

uint16_t const this_node = 00;

uint16_t children[4] = { };
unsigned child_count = 0;

unsigned long const PAIRING_MODE_TIMEOUT = 10000;
bool in_pairing_mode = false;
unsigned long pairing_mode_start_time = 0;


/* ==[ FUNCTIONS ]== */
uint16_t next_child(void);



void setup()
{
  Serial.begin(9600);
  radio.begin();
  network.begin(this_node);
  radio.setDataRate(RF24_2MBPS);

  pinMode(PIN_PAIR_BTN, INPUT_PULLUP);
}

static byte counter = 0x08;
static int delta = 8;
static byte led_state = 0;

void loop()
{
  network.update();

  /* receive messages */
  while (network.available())
  {
    /* read the message from the network */
    RF24NetworkHeader header;
    char message[32];
    network.read(header, &message, 32);
    Serial.print("Received ");
    Serial.println(message);

    interpret_message(header, message);
  }


  /* send messages */
  for (unsigned i = 0; i < child_count; ++i)
  {
    {
    RF24NetworkHeader header(children[i], ID_INSTRUCTION);

    Instruction inst(OP_WRITE_REGISTER);
    inst.data[0] = REG_SOUND;
    inst.data[1] = counter;

    int msg_size = 0;
    byte *msg = inst.to_message(&msg_size);

    network.write(header, msg, msg_size);
    delayMicroseconds(300);
    delete[] msg;
    }
    {
    RF24NetworkHeader header(children[i], ID_INSTRUCTION);

    Instruction inst(OP_WRITE_REGISTER);
    inst.data[0] = REG_LIGHT;
    inst.data[1] = led_state;

    int msg_size = 0;
    byte *msg = inst.to_message(&msg_size);

    network.write(header, msg, msg_size);
    delayMicroseconds(300);
    delete[] msg;
    }
  }

  if (counter >= 0xff - 8  || counter <= 0)
  {
    delta *= -1;

    led_state = led_state? 0 : 1;
  }
  counter += delta;


  // enter pairing mode if pairing button is clicked
  if (digitalRead(PIN_PAIR_BTN) == LOW)
  {
    in_pairing_mode = true;
    pairing_mode_start_time = millis();
    Serial.println("Entering pairing mode");
  }

  // exit pairing mode after a certain timeframe
  if (in_pairing_mode && millis() - pairing_mode_start_time > PAIRING_MODE_TIMEOUT)
  {
    in_pairing_mode = false;
    Serial.println("Leaving pairing mode");
  }

  delay(50);
}


/* 0:  number
 * 1:  parent #
 * 2:  grandparent #
 * 3:  great-grandparent #
 * 
 * each time this is called, it returns the next available network address
 * 
 * TODO: clean this up?
 */
uint16_t next_child(void)
{
  static uint8_t digits[4] = { 2, 0, 0, 0 };

  uint16_t addr = digits[0];

  if (digits[1] == 0)
  {
    addr = digits[0];
  }
  else if (digits[2] == 0)
  {
    addr = (digits[0] << 3) | digits[1];
  }
  else if (digits[3] == 0)
  {
    addr = (digits[0] << 6) | (digits[1] << 3) | digits[2];
  }
  else
  {
    addr = (digits[0] << 9) | (digits[1] << 6) | (digits[2] << 3) | digits[3];
  }

  for (int i = 0; i < 4; ++i)
  {
    digits[i]++;
    if (digits[i] > 5)
    {
      digits[i] = 1;
    }
    else
    {
      break;
    }
  }

  return addr;
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
     }break;

    /* write to a register */
    case OP_WRITE_REGISTER:
     {byte reg   = message[2],
           value = message[3];

      Serial.print("write 0x");
      Serial.print(value, HEX);
      Serial.print(" to register 0x");
      Serial.println(reg, HEX);
     }break;
    
    default:
      error("unknown opcode %.2hhX", opcode);
      break;
    }
   }break;

  /* button event */
  case ID_BUTTON_EVENT:
   {Serial.println("Button Event");
    ButtonEvent e;

    // read the message into the event object
    size_t offset = 1;
    memcpy (&e.time_ms, message + offset, sizeof(e.time_ms));
    offset += sizeof(e.time_ms);
    memcpy (&e.time_ms, message + offset, sizeof(e.time_us));
    offset += sizeof(e.time_us);
    e.team   = message[offset];
    e.player = message[offset+1];

    // TODO -- send the event to the computer
    Serial.print("Event occurred at ");
    Serial.print(e.time_ms);
    Serial.print("ms, ");
    Serial.print(e.time_us);
    Serial.print("us, player #");
    Serial.print(e.player);
    Serial.print(" on team #");
    Serial.print(e.team);
    Serial.println(".");
   }break;

  case ID_PING:
   {Serial.print("Got '");
    Serial.print((char*)message);
    Serial.println("'");

    RF24NetworkHeader response_header(header.from_node, ID_PING);
    char pong_msg[32] = "pong";
    network.write(response_header, pong_msg, sizeof(pong_msg));
    Serial.println("Pong!");

    RF24NetworkHeader null_header;
    byte null_msg[32];
    network.read(null_header, &null_msg, sizeof(null_msg));
   }break;

  case ID_PAIR:
   {Serial.println("Pairing request received");
    if (in_pairing_mode)
    {
      uint16_t addr = next_child();
  
      RF24NetworkHeader response_header(01, ID_PAIR);
      char pair_msg[32] = { addr & 0xFF, (addr >> 8) & 0xFF, 0 };
      network.write(response_header, pair_msg, sizeof(pair_msg));
  
      children[child_count++] = addr;
  
      Serial.print("New child is @ ");
      Serial.println(addr);
    }
    else
    {
      Serial.println("Not in pairing mode!");
    }
   }break;

  case ID_DISCONNECT:
   {Serial.println("Disconnect message received");
    // TODO -- properly remove the child
    child_count--;

    RF24NetworkHeader null_header;
    byte null_msg[32];
    network.read(null_header, &null_msg, sizeof(null_msg));
   }break;

  default:
    error("unknown message ID 0x%.2hhX", header.type);
    break;
  }
}




