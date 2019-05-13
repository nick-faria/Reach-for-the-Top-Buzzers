/*
 * Button Radio library
 *
 */


#include <arduino.h>

#include <stdarg.h>

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#include "button_radio.h"



/* error: error logging */
void error(char const *const format, ...)
{
  Serial.println("an error occurred");
  va_list ap;
  va_start(ap, format);

  char *out = NULL;
  int str_length = vsnprintf(out, 0, format, ap);

  out = (char*)calloc(1, str_length);
  vsnprintf(out, str_length, format, ap);

  Serial.print("ERROR: ");
  Serial.println(out);
  free(out);

  va_end(ap);
}



/* to_message(Instruction):  */
byte *Instruction::to_message(int *msg_size=nullptr)
{
  byte *msg = new byte[32];
  memset(msg, 0, 32);

  //Serial.print("Message is ");
  //Serial.print(this->op);
  //Serial.print(", ");
  //Serial.print((char*)this->data);
  //Serial.println("");

  /* create the message */
  msg[0] = ID_INSTRUCTION;
  msg[1] = this->op;
  memcpy(msg + 2, this->data, 30);

  if (msg_size != nullptr)
  {
    *msg_size = 32;
  }

  return msg;
}

/* to_message(ButtonEvent):  */
byte *ButtonEvent::to_message(int *msg_size=nullptr)
{
  byte *msg = new byte[32];
  memset(msg, 0, 32);

  /* create the message */
  unsigned offset = 0;

  //Serial.print("Message is ");
  //Serial.print(event.time_ms);
  //Serial.print(", ");
  //Serial.print(event.time_us);
  //Serial.print(", ");
  //Serial.print(event.team);
  //Serial.print(", ");
  //Serial.print(event.player);
  //Serial.println("");

  msg[0] = ID_BUTTON_EVENT;
  offset += 1;
  memcpy( msg + offset, &this->time_ms, sizeof(this->time_ms) );
  offset += sizeof(this->time_ms);
  memcpy( msg + offset, &this->time_us, sizeof(this->time_us) );
  offset += sizeof(this->time_us);
  msg[offset] = this->team;
  offset += 1;
  msg[offset] = this->player;


  if (msg_size != nullptr)
  {
    *msg_size = offset;
  }

  return msg;
}
