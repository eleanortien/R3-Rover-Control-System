#include <Ethernet.h>
#include <EthernetUdp.h>
#define UDP_TX_PACKET_MAX_SIZE 36 //increase UDP size
#include <SPI.h>
#include <Servo.h>

class motor{
  public:
    Servo servo;
    int pin;
};

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE };  //Assign a mac address
//IPAddress compIp(169, 254, 15, 133);                  //Find IP address (put in brackets) and assign IP address
IPAddress ardIp(192, 168, 1, 243);

unsigned int localPort = 8090;  //Assign port to talk over
//unsigned int pythonPort = 7000;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  //Sent Data
String dataReq;                             //String for data
int packetSize;
EthernetUDP udp;  //Define UDP Object

//Variable setup
int lw1, lw2, lw3, rw1, rw2, rw3;
int wheels[6] = {lw1, rw1, lw2, rw2, lw3, rw3}; 

Servo servoLW1, servoLW2, servoLW3, servoRW1, servoRW2, servoRW3;
Servo servoList [6]= {servoLW1, servoRW1, servoLW2, servoRW2, servoLW3, servoRW3};
motor motorL1, motorR1, motorL2, motorR2, motorL3, motorR3;
motor motors [6] = {motorL1, motorR1, motorL2, motorR2, motorL3, motorR3};

//Drive Pin Numbers
int leftW1 = 11;
int leftW2 = 12;
int leftW3 = 24;
int rightW1 = 25;
int rightW2 = 28;
int rightW3 = 29;
int ledRed = 33;
int ledBlue = 34;
int ledGreen = 35;


int pinList [9]={leftW1, rightW1, leftW2, rightW2, leftW3, rightW3, ledRed, ledBlue, ledGreen};
int motorSize = 6;




void setup() {
  //Serial.begin(115200);        //Turn on Serial Port
  Ethernet.begin(mac, ardIp);  //Initialise Ethernet
  udp.begin(localPort);        //Start udp
  delay(1500);
  for (int motor = 0; motor < motorSize; motor++)
  {
    motors[motor].servo = servoList[motor];
    motors[motor].pin = pinList[motor];
    motors[motor].servo.attach(motors[motor].pin);
  }
}

void loop() {
  packetSize = udp.parsePacket();  //Read packet size
  if (packetSize > 0) {
    udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    String data(packetBuffer);  //Convert data to string
    
    if (data.substring(0, data.indexOf("_")) == "DriveCommand")
    {
      data = data.substring(data.indexOf("_") + 1 );
      for (int i = 0; i < motorSize; i++)
      {
        int wheel = int(data[0, data.indexOf("_")]);
        wheels[i] = wheel;
        servoList[i].writeMicroseconds((int) (int(wheels[i])/255 * 1000) + 1000);
        data = data.substring(data.indexOf("_") + 1 );

      }

    }
    

    //Clear packet
    memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE);
  }
}














