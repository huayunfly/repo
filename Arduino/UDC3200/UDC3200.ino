/* Honeywell UDC3200 reading PV(Modbus addr 0x40) via RS-485
@Author: Yun Hua, huayunfly@126.com
@Date: 2017.01.05
*/
#include <ModbusMaster.h>

ModbusMaster node;

void setup() {
  // Use Serial (port 0); initialize Modbus communication baud rate
  Serial.begin(19200);

  // Communicate with Modbus slave ID 2 over Serial (port 0)
  node.begin(2, Serial);

}

void loop() {
  // Serial.println("hello");
  delay(3000);

  static uint32_t i;
  uint8_t j, result;
  uint16_t data[6];

  i++;

  // Set word 0 of TX buffer to least-significant word of counter (bits 15..0)
  //node.setTransmitBuffer(0, lowWord(i));

  // Set word 1 of TX buffer to most-significant word of counter (bits 31..16)
  //node.setTransmitBuffer(1, highWord(i));

  // Slave: write TX buffer to (2) 16-bit registers (IEEE 32bit float 100.0) starting at register 0x78 (Loop1 SP)
  node.setTransmitBuffer(0, 0x42C8);
  node.setTransmitBuffer(1, 0x0000);
  result = node.writeMultipleRegisters(0x78, 2);
  Serial.println(result, HEX); // Error code 0x06 may returned for the Slave Device Busy
  delay(5000);

  // Slave: read (2) 16-bit registers (IEEE 32bit float) starting at register 0x40 (Loop1 PV) to RX buffer
  //result = node.readInputRegisters(0x40, 2);
  
  // do something with data if read is successful
  if (result == node.ku8MBSuccess)
  {
    for (j = 0; j < 2; j++)
    {
      data[j] = node.getResponseBuffer(j);
    }
    // IEEE 32-bit Floating-Point Register Information
    // data[0] = 0x4189, data[1] = 0xEC00
    // 0x4189EC00 : 0100 0001     1000  1001 1110 1100 0000 0000
    // 0x4189EC00 : 0 1000 0011 (implied 1.)000 1001 1110 1100 0000 0000
    // binary number: implied 1 + 0*2^-1 + 0*2e-2 + 0*2e-3 + 1*2e-4 + 0*2e-5 + 0*2e-6 + 1*2e-7
    // exponent: 1*2^7 + ... + 1*2^1 + 1*2^0 = 131; exponent = 131 - 127(bias) = 4
    // float value = binary number * 2^exponent = 17.24
    //Serial.println(data[0], HEX);
    delay(100);
    //Serial.println(data[1], HEX);
    delay(100);
  }


}
