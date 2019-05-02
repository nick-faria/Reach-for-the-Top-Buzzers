/*
 * thing
 *
 */

#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>

#include <button_radio.h>


enum
{
  PIN_CE  = 7,
  PIN_CSN = 8,
};


RF24 radio(PIN_CE, PIN_CSN);
RF24Network network(radio);

uint16_t const this_node = 00;

uint16_t const child[] = { 01, 02 };
unsigned child_count = 2;



void setup()
{
  Serial.begin(9600);
  radio.begin();
  network.begin(this_node);
  radio.setDataRate(RF24_2MBPS);
}

void loop()
{
  network.update();

  /* receive messages */
  while (network.available())
  {
    RF24NetworkHeader header;
    char recv[12];
    network.read(header, &recv, 12);
    Serial.print("Received ");
    Serial.println(recv);

    network.update();
  }


  /* send messages */
  for (unsigned i = 0; i < child_count; ++i)
  {
    RF24NetworkHeader header(child[i], ID_INSTRUCTION);

    Instruction inst(OP_WRITE_REGISTER);
    inst.data[0] = 0x80;

    int msg_size = 0;
    byte *msg = inst.to_message(&msg_size);

    network.write(header, msg, msg_size);
    delete[] msg;
  }

  delay(50);
}

