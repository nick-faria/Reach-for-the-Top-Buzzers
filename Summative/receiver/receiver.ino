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

#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>

#include <button_radio.h>


/* ==[ VARIABLES ]== */
/* pins */
enum
{
  PIN_CE     = 7,
  PIN_CSN    = 6,

  PIN_LIGHT  = 9,
  PIN_SOUND  = 5,

  PIN_BUTTON = 8,
};


RF24 radio(PIN_CE, PIN_CSN);
RF24Network network(radio);

uint16_t       this_node = 01;
uint16_t const parent    = 00;

uint8_t this_team = 0;


bool can_be_pressed  = true;

int  button_previous = HIGH;
bool button_is_held = false;
unsigned long button_pressed_time = 0;
unsigned long const PAIRING_MODE_START_DELAY = 1000;

byte registers[REGISTER_COUNT];


/* ==[ FUNCTIONS ]== */
void interpret_message(RF24NetworkHeader header, byte *message);
bool pair(void);



void setup()
{
  Serial.begin(9600);
  radio.begin();
  radio.setDataRate(RF24_2MBPS);

  network.multicastLevel(this_team);

  pinMode(PIN_LIGHT   , OUTPUT);
  pinMode(PIN_BUTTON  , INPUT_PULLUP);

  debug("Initialized");
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
    debug("Reading...");
    network.read(header, &message, 32);
    debug("Received '%s'", message);

    interpret_message(header, message);
  }

  /* handle the button -- when pressed, it sends an event to the server.
     If it is held for long enough, the unit will enter pairing mode */
  int button_state = digitalRead(PIN_BUTTON);
  if (button_state != button_previous)
  {
    debug("button pushed");

    /* the button was pressed */
    if (button_state == LOW)
    {
      button_pressed_time = millis();
      button_is_held = true;

      /* send a button press event to the server */
      if (can_be_pressed)
      {
        can_be_pressed = false;
        RF24NetworkHeader header(parent, ID_BUTTON_EVENT);
    
        ButtonEvent btn_event(this_team, this_player);
        int msg_size = 0;
        byte *msg = btn_event.to_message(&msg_size);
    
        network.write(header, msg, msg_size);
        delayMicroseconds(300);
        delete[] msg;
        debug("button pressed");

        registers[REG_LIGHT] = 0x01;
        registers[REG_SOUND] = 0x10;
      }
    }
    /* button was released */
    else
    {
      button_is_held = false;
      registers[REG_LIGHT] = 0x00;
      registers[REG_SOUND] = 0x00;
    }
  }
  button_previous = button_state;

  /* after the button has been held for a certain amount of time, attempt to pair */
  if (button_is_held && millis() - button_pressed_time >= PAIRING_MODE_START_DELAY)
  {
    /* hold our previous address, so we can reuse
     * our old address if we fail to pair */
    uint16_t previous_address = this_node;
    uint8_t  previous_team    = this_team;
    if (!pair())
    {
      debug("Failed to pair!");
      this_node = previous_address;
      this_team = previous_team;
      network.begin(this_node);
      network.multicastLevel(this_team);
    }
    else
    {
      button_is_held = false;
      can_be_pressed = true;
    }
  }

  /* update the registers */
  digitalWrite(PIN_LIGHT, registers[REG_LIGHT]);
  if (registers[REG_SOUND] == 0x00)
  {
    noTone(PIN_SOUND);
  }
  else
  {
    int pitch = map(registers[REG_SOUND], 0, 255, 512, 1024);
    tone(PIN_SOUND, pitch);
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
     {
      debug("New Question");
      can_be_pressed = true;
     }break;

    /* write to a register */
    case OP_WRITE_REGISTER:
     {byte reg   = message[2],
           value = message[3];

      debug("write 0x%h to register 0x%h", value, reg);

      registers[reg] = value;
     }break;
    
    default:
      error("unknown opcode %.2hhX", opcode);
      break;
    }
   }break;

  default:
    error("unknown message ID 0x%.2hhX", header.type);
    break;
  }
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

  /* store our old name */
  uint16_t old_name = this_node;

  /* Node 01 is reserved for pairing */
  network.begin(01);

  /* make sure there is a server to pair with */
  if (ping())
  {
    debug("requesting new address!");

    /* request to pair with the server */
    RF24NetworkHeader pair_header(parent, ID_PAIR);
    char pair_msg[32] = "";
    network.write(pair_header, pair_msg, sizeof(pair_msg));

    /* wait for the pairing message from the server */
    bool got_pair_response = true;
    unsigned long const PAIRING_TIMEOUT = 1000;
    unsigned long pairing_begin = millis();
    network.update();
    while (!network.available())
    {
      debug("%lu", millis() - pairing_begin);
      if (millis() - pairing_begin > PAIRING_TIMEOUT)
      {
        got_pair_response = false;
        break;
      }
      network.update();
    }

    if (got_pair_response)
    {
      /* receive our new address */
      uint16_t address = 0;
      uint8_t  team    = 0;
      byte addr_data[sizeof(address) + sizeof(team)] = { 0 };

      RF24NetworkHeader recv_header;
      network.read(recv_header, &addr_data, sizeof(addr_data));

      memcpy(&address, addr_data, sizeof(address));
      memcpy(&team, addr_data + sizeof(address), sizeof(team));

      debug("new address is %d on team %d", address, team);

      /* set our new address */
      network.begin(address);
      network.multicastLevel(team);
  
      /* ensure we can connect to the server with our new address */
      if (ping())
      {
        /* send a disconnect message to the current parent, to free our old name */
        RF24NetworkHeader discon_header(parent, ID_DISCONNECT);
        byte discon_msg[32];
        memcpy (discon_msg, &old_name, sizeof(old_name));
        network.write(discon_header, discon_msg, sizeof(discon_msg));

        this_node = address;
        this_team = team;
        return true;
      }
      else
      {
        debug("Didn't receive pong after setting new address");
      }
    }
    else
    {
      debug("Didn't receive new address");
    }
  }
  /* we were not acknowledged */
  else
  {
    debug("Server pong timed out!");
  }

  return false;
}

/* ping: ping the server */
bool ping(void)
{
  unsigned long const PING_TIMEOUT = 1000;

  /* try to ping the server */
  RF24NetworkHeader ping_header(parent, ID_PING);
  char ping[32] = "ping";
  network.write(ping_header, ping, sizeof(ping));
  debug("Ping!");

  unsigned long start = millis();


  /* wait for the pong from the server */
  network.update();
  while (!network.available())
  {
    network.update();
    if (millis() - start > PING_TIMEOUT)
    {
      debug("ping() -- didn't receive a pong");
      return false;
    }
  }

  /* receive the pong from the server */
  RF24NetworkHeader pong_header;
  char pong[32];
  network.read(pong_header, &pong, sizeof(pong));

  debug("ping() -- got a pong");
  return true;
}

