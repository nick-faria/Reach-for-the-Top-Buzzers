/*
 * Button Radio library
 *
 */


#ifndef _TEST_H
#define _TEST_H


/* ==[ ENUMS ]== */

/* ID_Types
 *  enum for message identifiers
 */
enum ID_Types
{
  ID_INSTRUCTION  = 0x00,
  ID_BUTTON_EVENT,
};

/* Opcodes:
 *  opcodes
 */
enum Opcodes
{
  OP_NEW_QUESTION   = 0x00,
  OP_WRITE_REGISTER,
};

/* Registers:
 *  register IDs
 */
enum Registers
{
  REG_LIGHT  = 0x00,
  REG_SOUND,
  REG_ENABLE,

  REGISTER_COUNT,  /* dummy, counts how many registers there are */
};



/* ==[ CLASSES ]== */

/* ButtonEvent:
 *  messages from player to server
 *  contains button event data
 */
class ButtonEvent
{
public:
  unsigned long time_ms;
  unsigned long time_us;
  byte team;
  byte player;

  ButtonEvent()
 : time_ms(0),
   time_us(0),
   team(0),
   player(0)
  {
  }

  ButtonEvent(int _team, int _player)
 : time_ms(millis()),
   time_us(micros() % 1000),
   team(_team),
   player(_player)
  {
  }
};

/* Instruction:
 *  messages from server to players
 *  contains instruction data
 */
class Instruction
{
public:
  byte op;
  byte data[30];

  Instruction(byte _op)
 : op(_op)
  {
    memset(data, 0, sizeof(data));
  }
};



/* ==[ FUNCTIONS ]== */
void error(char const *const format, ...);

bool send_message(RF24 radio, byte const addr[6], Instruction inst);
bool send_message(RF24 radio, byte const addr[6], ButtonEvent event);


#endif
