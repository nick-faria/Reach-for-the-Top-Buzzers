/*
 * Button Radio library
 *
 */


#ifndef _BUTTON_RADIO_H
#define _BUTTON_RADIO_H


/* ==[ ENUMS ]== */

/* ID_Types
 *  enum for message identifiers
 */
enum ID_Types
{
  ID_INSTRUCTION  = 0x00,
  ID_BUTTON_EVENT,
  ID_PING,
  ID_PAIR,
  ID_DISCONNECT,
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
  uint32_t time_ms;
  uint32_t time_us;

  byte *to_message(int *msg_size);

  ButtonEvent()
 : time_ms(0),
   time_us(0)
  {
  }

  ButtonEvent(int _team, int _player)
 : time_ms(millis()),
   time_us(micros() % 1000)
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

  byte *to_message(int *msg_size);

  Instruction(byte _op, byte *_data=nullptr)
 : op(_op)
  {
    memset(data, 0, sizeof(data));
    if (_data != nullptr)
    {
      memcpy(data, _data, 30);
    }
  }
};



/* ==[ FUNCTIONS ]== */
void debug(char const *const format, ...);
void error(char const *const format, ...);


#endif
