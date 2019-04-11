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



byte *create_message(Instruction instr);
byte *create_message(ButtonEvent event);
bool send_bytes(RF24 radio, byte const addr[6], byte const data[32]);



/* error: error logging */
void error(char const *const format, ...)
{
  Serial.println("an error occurred");
  va_list ap;
  va_start(ap, format);

  char *out = NULL;
  int str_length = vsnprintf(out, 0, format, ap);

  out = calloc(1, str_length);
  vsnprintf(out, str_length, format, ap);

  Serial.print("ERROR: ");
  Serial.println(out);
  free(out);

  va_end(ap);
}

/* send_message(Instruction):  */
bool send_message(RF24 radio, byte const addr[6], Instruction instr)
{
  byte *msg = create_message(instr);
  bool success = send_bytes(radio, addr, msg);
  delete[] msg;
  return success;
}

/* send_message(ButtonEvent):  */
bool send_message(RF24 radio, byte const addr[6], ButtonEvent event)
{
  byte *msg = create_message(event);
  bool success = send_bytes(radio, addr, msg);
  delete[] msg;
  return success;
}

/* create_message(Instruction):  */
byte *create_message(Instruction instr)
{
  byte *msg = new byte[32];
  memset(msg, 0, 32);

  //Serial.print("Message is ");
  //Serial.print(inst.op);
  //Serial.print(", ");
  //Serial.print((char*)inst.data);
  //Serial.println("");

  /* create the message */
  msg[0] = ID_INSTRUCTION;
  msg[1] = instr.op;
  memcpy(msg + 2, instr.data, 30);

  return msg;
}

/* create_message(ButtonEvent):  */
byte *create_message(ButtonEvent event)
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
  memcpy( msg + offset, &event.time_ms, sizeof(event.time_ms) );
  offset += sizeof(event.time_ms);
  memcpy( msg + offset, &event.time_us, sizeof(event.time_us) );
  offset += sizeof(event.time_us);
  msg[offset] = event.team;
  offset += 1;
  msg[offset] = event.player;

  return msg;
}

/* send_bytes: write bytes to the TX FIFO */
bool send_bytes(RF24 radio, byte const addr[6], byte const *data)
{
  radio.openWritingPipe(addr);

  radio.stopListening();
  bool success = radio.write(data, 32);
  radio.startListening();

  return success;
}
