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
 */

#include <SPI.h>
#include <RF24Network.h>
#include <RF24.h>

#include <button_radio.h>

/* TODO: set this to 1 in deployment!
 * disable the debug and error messages so they don't get sent to the host */
#if 0
#define debug(fmt, ...) ({ })
#define error(fmt, ...) ({ })
#endif


/* ==[ VARIABLES ]== */
/* pins */
enum
{
  PIN_CE  = 7,
  PIN_CSN = 8,

  PIN_PAIR_BTN_TEAM_1 = 5,
  PIN_PAIR_BTN_TEAM_2 = 4,
};


RF24 radio(PIN_CE, PIN_CSN);
RF24Network network(radio);

uint16_t const this_node = 00;

size_t const MAXIMUM_CHILDREN = 4;
uint16_t children[2][MAXIMUM_CHILDREN] = { { }, { } };
unsigned child_count[2] = { 0, 0 };

unsigned long const PAIRING_MODE_TIMEOUT = 10000;
bool in_pairing_mode = false;
unsigned long pairing_mode_start_time = 0;
int pairing_team = 0;

uint8_t button_mask = 0x00;

int pressed_button = -1;



void setup()
{
  Serial.begin(9600);
  radio.begin();
  network.begin(this_node);
  radio.setDataRate(RF24_2MBPS);

  pinMode(PIN_PAIR_BTN_TEAM_1, INPUT_PULLUP);
  pinMode(PIN_PAIR_BTN_TEAM_2, INPUT_PULLUP);

  debug("Initialized");
}

static byte counter = 0x08;
static int delta = 8;
static byte led_state = 0;
static unsigned long note_change_time = 0;

void loop()
{
  network.update();

  /* receive messages from the network */
  while (network.available())
  {
    /* read the message from the network */
    RF24NetworkHeader header;
    char message[32];
    network.read(header, &message, 32);
    debug("Received '%s'", message);

    interpret_message(header, (byte *)message);
  }

  /* receive messages from the computer; these are always just a button mask, and are only
     sent at the start of a new question */
  while (Serial.available())
  {
    byte serial_msg = Serial.read();
    button_mask = serial_msg;
    pressed_button = -1;

    /* these messages mark the beginning of a new question */
    Instruction inst(OP_NEW_QUESTION);
    int msg_size = 0;
    byte *msg = inst.to_message(&msg_size);

    RF24NetworkHeader header(00, ID_INSTRUCTION);
    network.multicast(header, msg, msg_size, 0);
    network.multicast(header, msg, msg_size, 1);
    delete[] msg;
  }

  /* read each pairing button */
  int team_1_pair = digitalRead(PIN_PAIR_BTN_TEAM_1) == LOW,
      team_2_pair = digitalRead(PIN_PAIR_BTN_TEAM_2) == LOW;

  /* enter pairing mode if pairing button is clicked */
  if (team_1_pair && team_2_pair)
  {
    debug("Can't pair both teams simultaneously!");
  }
  else if (team_1_pair || team_2_pair)
  {
    in_pairing_mode = true;
    pairing_mode_start_time = millis();
    pairing_team = team_1_pair? 0 : 1;
    debug("Entering pairing mode (Team %d)", pairing_team + 1);
  }

  /* exit pairing mode after a certain timeframe */
  if (in_pairing_mode && millis() - pairing_mode_start_time > PAIRING_MODE_TIMEOUT)
  {
    in_pairing_mode = false;
    debug("Leaving pairing mode");
  }

  delay(100);
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
  /* button event */
  case ID_BUTTON_EVENT:
   {
    debug("Button Event");
    ButtonEvent e;

    int team   = 0,
        player = 0;

    /* read the message into the event object */
    size_t offset = 1;
    memcpy (&e.time_ms, message + offset, sizeof(e.time_ms));
    offset += sizeof(e.time_ms);
    memcpy (&e.time_ms, message + offset, sizeof(e.time_us));

    for (int team = 0; team < 2; ++team)
    {
      for (int i = 0; i < MAXIMUM_CHILDREN; ++i)
      {
        if (children[team][i] == header.from_node)
        {
          team = team;
          player = i;
          goto buttonevent_done_searching_for_child;
        }
      }
    }
buttonevent_done_searching_for_child:

    uint8_t button_number = (team * 4) + player;

    /* make sure  this button isn't masked off */
    if (button_mask & ( 1 << button_number ) != 0)
    {
      /* we haven't sent an event to the computer yet, so send this one */
      if (pressed_button == -1)
      {
        pressed_button = button_number;
      }
    }

    debug("Event occurred at %lums, %luus, player #%d on team #%d.",
          e.time_ms, e.time_us, player + 1, team + 1);
   }break;

  case ID_PING:
   {
    debug("Got '%s'", (char*)message);

    RF24NetworkHeader response_header(header.from_node, ID_PING);
    char pong_msg[32] = "pong";
    network.write(response_header, pong_msg, sizeof(pong_msg));
    debug("Pong!");

    RF24NetworkHeader null_header;
    byte null_msg[32];
    network.read(null_header, &null_msg, sizeof(null_msg));
   }break;

  case ID_PAIR:
   {
    debug("Pairing request received");
    if (in_pairing_mode)
    {
      /* make sure there's space on the team */
      if (child_count[pairing_team] < MAXIMUM_CHILDREN)
      {
        uint16_t addr = next_child();
    
        RF24NetworkHeader response_header(01, ID_PAIR);
        char pair_msg[32] = { (char)(addr & 0xFF), (char)((addr >> 8) & 0xFF),
                              (char)pairing_team & 0xFF };
        network.write(response_header, pair_msg, sizeof(pair_msg));
  
        children[pairing_team][child_count[pairing_team]++] = addr;
    
        debug("New child is @ %d on team %d", addr, pairing_team);
      }
      else
      {
        error("Can't pair -- team %d is full!", pairing_team + 1);
      }
    }
    else
    {
      error("Can't pair -- not in pairing mode!");
    }
    RF24NetworkHeader null_header;
    byte null_msg[32];
    network.read(null_header, &null_msg, sizeof(null_msg));
   }break;

  case ID_DISCONNECT:
   {
    debug("Disconnect message received");

    /* get the address to remove */
    uint16_t discon_addr = 0;
    memcpy(&discon_addr, message, sizeof(discon_addr));

    debug("address to remove is %d", discon_addr);

    /* try to remove the child */
    for (int team = 0; team < 2; ++team)
    {
      for (int i = 0; i < child_count[team]; ++i)
      {
        if (children[team][i] == discon_addr)
        {
          debug("removing child #%d", discon_addr);
          children[team][i] = 0;
  
          memmove(children[team] + i , children[team] + i + 1, child_count[team] - i - 1);
          child_count[team]--;
          goto disconnect_done_searching_for_child;
        }
      }
    }
disconnect_done_searching_for_child:
    ;
   }break;

  default:
    error("Unknown or invalid message type 0x%.2hhX", header.type);
    break;
  }
}

